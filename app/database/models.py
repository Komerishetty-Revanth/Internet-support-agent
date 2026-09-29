from sqlalchemy import Column, String, Integer, DateTime, Text, Boolean, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from .database import Base

class IssueCategory(str, enum.Enum):
    """Issue categories"""
    NO_INTERNET = "NO_INTERNET"
    SLOW_INTERNET = "SLOW_INTERNET"
    WIFI_NO_INTERNET = "WIFI_NO_INTERNET"
    INTERMITTENT = "INTERMITTENT"
    ROUTER_PROBLEM = "ROUTER_PROBLEM"
    CABLE_PROBLEM = "CABLE_PROBLEM"
    DEVICE_PROBLEM = "DEVICE_PROBLEM"
    NETWORK_CONFIGURATION = "NETWORK_CONFIGURATION"
    POSSIBLE_ISP_PROBLEM = "POSSIBLE_ISP_PROBLEM"
    UNKNOWN = "UNKNOWN"

class TroubleshootingStage(str, enum.Enum):
    """Troubleshooting stages"""
    START = "START"
    CLASSIFY = "CLASSIFY"
    DIAGNOSE = "DIAGNOSE"
    TROUBLESHOOT = "TROUBLESHOOT"
    VERIFY = "VERIFY"
    RESOLVED = "RESOLVED"
    ESCALATED = "ESCALATED"

class Customer(Base):
    """Customer model"""
    __tablename__ = "customers"
    
    id = Column(String, primary_key=True, index=True)
    email = Column(String, index=True)
    name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    conversations = relationship("Conversation", back_populates="customer")
    troubleshooting_sessions = relationship("TroubleshootingSession", back_populates="customer")

class Conversation(Base):
    """Conversation/chat session"""
    __tablename__ = "conversations"
    
    id = Column(String, primary_key=True, index=True)
    customer_id = Column(String, ForeignKey("customers.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    customer = relationship("Customer", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")
    troubleshooting_session = relationship("TroubleshootingSession", back_populates="conversation", uselist=False)

class Message(Base):
    """Individual message in conversation"""
    __tablename__ = "messages"
    
    id = Column(String, primary_key=True, index=True)
    conversation_id = Column(String, ForeignKey("conversations.id"))
    role = Column(String)  # "customer" or "agent"
    content = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    conversation = relationship("Conversation", back_populates="messages")

class TroubleshootingSession(Base):
    """Troubleshooting session state"""
    __tablename__ = "troubleshooting_sessions"
    
    id = Column(String, primary_key=True, index=True)
    customer_id = Column(String, ForeignKey("customers.id"))
    conversation_id = Column(String, ForeignKey("conversations.id"), unique=True)
    
    # Troubleshooting state
    issue_category = Column(Enum(IssueCategory), nullable=True)
    stage = Column(Enum(TroubleshootingStage), default=TroubleshootingStage.START)
    current_step = Column(Integer, default=0)
    
    # Status
    resolved = Column(Boolean, default=False)
    escalated = Column(Boolean, default=False)
    escalation_reason = Column(Text, nullable=True)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    customer = relationship("Customer", back_populates="troubleshooting_sessions")
    conversation = relationship("Conversation", back_populates="troubleshooting_session")