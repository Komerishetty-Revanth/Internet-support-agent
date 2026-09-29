from sqlalchemy.orm import Session
from app.database.models import (
    Customer, Conversation, Message, TroubleshootingSession,
    TroubleshootingStage
)
from app.agent.troubleshooter import troubleshooter
import uuid
from datetime import datetime


class SupportService:
    """Main support service that orchestrates the workflow"""
    
    @staticmethod
    def classify_by_keywords(message: str) -> str:
        """Simple keyword-based classification without API"""
        msg_lower = message.lower()
        
        if "slow" in msg_lower or "speed" in msg_lower:
            return "SLOW_INTERNET"
        elif "wifi" in msg_lower and "no internet" in msg_lower:
            return "WIFI_NO_INTERNET"
        elif "disconnect" in msg_lower or "keeps dropping" in msg_lower or "intermittent" in msg_lower:
            return "INTERMITTENT"
        elif "router" in msg_lower and ("problem" in msg_lower or "broken" in msg_lower):
            return "ROUTER_PROBLEM"
        elif "cable" in msg_lower or "connection" in msg_lower:
            return "CABLE_PROBLEM"
        elif "one device" in msg_lower or "only one" in msg_lower:
            return "DEVICE_PROBLEM"
        elif "dns" in msg_lower or "ip" in msg_lower or ("network" in msg_lower and "config" in msg_lower):
            return "NETWORK_CONFIGURATION"
        elif "not working" in msg_lower or "no internet" in msg_lower or "down" in msg_lower:
            return "NO_INTERNET"
        else:
            return "UNKNOWN"
    
    @staticmethod
    def create_or_get_customer(db: Session, customer_id: str, email: str = "", name: str = "") -> Customer:
        """Create or retrieve a customer"""
        customer = db.query(Customer).filter(Customer.id == customer_id).first()
        if not customer:
            customer = Customer(id=customer_id, email=email, name=name)
            db.add(customer)
            db.commit()
        return customer
    
    @staticmethod
    def create_conversation(db: Session, customer_id: str) -> Conversation:
        """Create a new conversation"""
        conversation = Conversation(
            id=str(uuid.uuid4()),
            customer_id=customer_id
        )
        db.add(conversation)
        db.commit()
        return conversation
    
    @staticmethod
    def add_message(db: Session, conversation_id: str, role: str, content: str) -> Message:
        """Add message to conversation"""
        message = Message(
            id=str(uuid.uuid4()),
            conversation_id=conversation_id,
            role=role,
            content=content
        )
        db.add(message)
        db.commit()
        return message
    
    @staticmethod
    def create_troubleshooting_session(db: Session, customer_id: str, conversation_id: str, issue_category: str) -> TroubleshootingSession:
        """Create troubleshooting session"""
        session = TroubleshootingSession(
            id=str(uuid.uuid4()),
            customer_id=customer_id,
            conversation_id=conversation_id,
            issue_category=issue_category,
            stage=TroubleshootingStage.DIAGNOSE,
            current_step=0
        )
        db.add(session)
        db.commit()
        return session
    
    @staticmethod
    def update_session_stage(db: Session, session_id: str, stage: TroubleshootingStage, step: int = None) -> TroubleshootingSession:
        """Update troubleshooting session stage"""
        session = db.query(TroubleshootingSession).filter(TroubleshootingSession.id == session_id).first()
        if session:
            session.stage = stage
            if step is not None:
                session.current_step = step
            session.updated_at = datetime.utcnow()
            db.commit()
        return session
    
    @staticmethod
    def mark_escalated(db: Session, session_id: str, reason: str = "") -> TroubleshootingSession:
        """Mark session as escalated"""
        session = db.query(TroubleshootingSession).filter(TroubleshootingSession.id == session_id).first()
        if session:
            session.escalated = True
            session.stage = TroubleshootingStage.ESCALATED
            session.escalation_reason = reason
            session.updated_at = datetime.utcnow()
            db.commit()
        return session
    
    @staticmethod
    def get_next_agent_message(db: Session, customer_id: str, user_message: str) -> dict:
        """
        Get agent's next message based on conversation state.
        Returns: {message, issue_category, stage, resolved, escalated, step}
        """
        try:
            # Get or create customer
            customer = SupportService.create_or_get_customer(db, customer_id)
            
            # Get existing conversation or create new one
            conversation = db.query(Conversation).filter(
                Conversation.customer_id == customer_id
            ).order_by(Conversation.created_at.desc()).first()
            
            if not conversation:
                conversation = SupportService.create_conversation(db, customer_id)
            
            # Add user message
            SupportService.add_message(db, conversation.id, "customer", user_message)
            
            # Check if conversation already has a troubleshooting session
            ts_session = db.query(TroubleshootingSession).filter(
                TroubleshootingSession.conversation_id == conversation.id
            ).first()
            
            if not ts_session:
                # Create NEW session only if one doesn't exist
                # Simple keyword-based classification (without Grok)
                issue_category = SupportService.classify_by_keywords(user_message)
                
                ts_session = SupportService.create_troubleshooting_session(
                    db, customer_id, conversation.id, issue_category
                )
                
                # First response
                agent_message = f"Thank you for describing your issue. Let me help you troubleshoot. {troubleshooter.get_next_question(issue_category, 0)}"
            
            else:
                # Session exists - continue troubleshooting
                current_step = ts_session.current_step
                issue_category = ts_session.issue_category
                
                # Check if should escalate
                if troubleshooter.should_escalate(issue_category, current_step):
                    reason = troubleshooter.get_escalation_reason(issue_category)
                    SupportService.mark_escalated(db, ts_session.id, reason)
                    agent_message = f"Thank you for working through these steps with me. {reason} A technical support specialist will contact you shortly."
                    ts_session = db.query(TroubleshootingSession).filter(TroubleshootingSession.id == ts_session.id).first()
                else:
                    # Move to next step
                    next_step = current_step + 1
                    SupportService.update_session_stage(db, ts_session.id, TroubleshootingStage.TROUBLESHOOT, next_step)
                    agent_message = troubleshooter.get_next_question(issue_category, next_step)
                    ts_session = db.query(TroubleshootingSession).filter(TroubleshootingSession.id == ts_session.id).first()
            
            # Add agent message to DB
            SupportService.add_message(db, conversation.id, "agent", agent_message)
            
            return {
                "message": agent_message,
                "issue_category": ts_session.issue_category,
                "stage": ts_session.stage.value,
                "resolved": ts_session.resolved,
                "escalated": ts_session.escalated,
                "step": ts_session.current_step
            }
        
        except Exception as e:
            print(f"Support service error: {e}")
            import traceback
            traceback.print_exc()
            raise


# Global instance
support_service = SupportService()