from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database.database import get_db
from app.services.support_service import support_service

router = APIRouter(prefix="/api", tags=["chat"])

class ChatRequest(BaseModel):
    """Chat message request"""
    customer_id: str
    message: str
    email: str = ""
    name: str = ""

class ChatResponse(BaseModel):
    """Chat message response"""
    message: str
    issue_category: str = None
    stage: str
    resolved: bool
    escalated: bool
    step: int = None

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    """
    Handle customer support chat message.
    
    Flow:
    1. Create/get customer
    2. Create/get conversation
    3. Classify issue (if new)
    4. Generate next troubleshooting step
    5. Return agent response
    """
    try:
        # Validate input
        if not request.customer_id or not request.message:
            raise HTTPException(status_code=400, detail="customer_id and message required")
        
        if len(request.message.strip()) == 0:
            raise HTTPException(status_code=400, detail="message cannot be empty")
        
        # Create/get customer
        customer = support_service.create_or_get_customer(
            db,
            customer_id=request.customer_id,
            email=request.email,
            name=request.name
        )
        
        # Get next agent message (orchestrates entire flow)
        result = support_service.get_next_agent_message(
            db,
            customer_id=request.customer_id,
            user_message=request.message
        )
        
        return ChatResponse(
            message=result["message"],
            issue_category=result.get("issue_category"),
            stage=result["stage"],
            resolved=result["resolved"],
            escalated=result["escalated"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail="Error processing message")

@router.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "ok"}