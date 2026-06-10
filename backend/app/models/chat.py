"""
Chat models for Talk to Me platform.

This module contains models for managing chat sessions, messages, and AI responses.
"""

from datetime import datetime
from enum import Enum
from typing import Optional

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SQLEnum, Boolean, Float
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class MessageType(str, Enum):
    """Enum for message types."""
    TEXT = "text"
    AUDIO = "audio"
    IMAGE = "image"
    DOCUMENT = "document"


class SentimentScore(str, Enum):
    """Enum for sentiment analysis scores."""
    VERY_NEGATIVE = "very_negative"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    POSITIVE = "positive"
    VERY_POSITIVE = "very_positive"


class ChatSession:
    """
    Represents a chat session between a user and the AI assistant.
    
    Attributes:
        id: Unique identifier for the chat session
        user_id: Foreign key to the User who initiated the session
        started_at: Timestamp when the session started
        ended_at: Timestamp when the session ended (NULL if ongoing)
        is_active: Boolean indicating if the session is still active
        language: Language code for the session
        theme: Category or topic of the chat
        messages: Relationship to ChatMessage objects
    """
    __tablename__ = 'chat_sessions'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    ended_at = Column(DateTime, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    language = Column(String(10), default='en', nullable=False)
    theme = Column(String(100), nullable=True)
    summary = Column(Text, nullable=True)
    
    # Relationships
    user = relationship('User', backref='chat_sessions')
    messages = relationship('ChatMessage', back_populates='session', cascade='all, delete-orphan')
    ai_responses = relationship('AIResponse', back_populates='chat_session', cascade='all, delete-orphan')
    
    def __repr__(self) -> str:
        return f"<ChatSession id={self.id} user_id={self.user_id} active={self.is_active}>"
    
    def to_dict(self) -> dict:
        """Convert chat session to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'ended_at': self.ended_at.isoformat() if self.ended_at else None,
            'is_active': self.is_active,
            'language': self.language,
            'theme': self.theme,
            'summary': self.summary
        }


class ChatMessage:
    """
    Represents a single message in a chat session.
    
    Attributes:
        id: Unique identifier for the message
        session_id: Foreign key to the ChatSession
        sender_type: Either 'user' or 'assistant'
        message_type: Type of message (text, audio, image, document)
        content: The actual message content
        created_at: Timestamp when the message was created
        sentiment: Detected sentiment of the message
        confidence: Confidence score of sentiment detection
    """
    __tablename__ = 'chat_messages'
    
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey('chat_sessions.id'), nullable=False)
    sender_type = Column(String(20), nullable=False)  # 'user' or 'assistant'
    message_type = Column(SQLEnum(MessageType), default=MessageType.TEXT, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    sentiment = Column(SQLEnum(SentimentScore), nullable=True)
    confidence = Column(Float, nullable=True)
    is_flagged = Column(Boolean, default=False)  # For inappropriate content
    
    # Relationships
    session = relationship('ChatSession', back_populates='messages')
    
    def __repr__(self) -> str:
        return f"<ChatMessage id={self.id} sender={self.sender_type} type={self.message_type}>"
    
    def to_dict(self) -> dict:
        """Convert message to dictionary."""
        return {
            'id': self.id,
            'session_id': self.session_id,
            'sender_type': self.sender_type,
            'message_type': self.message_type.value if self.message_type else None,
            'content': self.content,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'sentiment': self.sentiment.value if self.sentiment else None,
            'confidence': self.confidence,
            'is_flagged': self.is_flagged
        }


class AIResponse:
    """
    Represents an AI-generated response to a user message.
    
    Attributes:
        id: Unique identifier for the response
        chat_session_id: Foreign key to the ChatSession
        user_message: The user's original message
        ai_message: The AI's response message
        model_used: Which AI model generated the response
        confidence: Confidence score of the AI response
        risk_level: Assessed risk level (e.g., 'low', 'medium', 'high', 'critical')
        action_recommended: Any recommended action for the platform
        generated_at: Timestamp when the response was generated
    """
    __tablename__ = 'ai_responses'
    
    id = Column(Integer, primary_key=True)
    chat_session_id = Column(Integer, ForeignKey('chat_sessions.id'), nullable=False)
    user_message_id = Column(Integer, ForeignKey('chat_messages.id'), nullable=False)
    ai_message_id = Column(Integer, ForeignKey('chat_messages.id'), nullable=False)
    model_used = Column(String(100), nullable=False)
    confidence = Column(Float, nullable=False)
    risk_level = Column(String(20), nullable=True)  # 'low', 'medium', 'high', 'critical'
    action_recommended = Column(String(255), nullable=True)
    generated_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    response_time_ms = Column(Integer, nullable=True)  # Response generation time
    
    # Relationships
    chat_session = relationship('ChatSession', back_populates='ai_responses')
    user_message = relationship('ChatMessage', foreign_keys=[user_message_id])
    ai_message = relationship('ChatMessage', foreign_keys=[ai_message_id])
    
    def __repr__(self) -> str:
        return f"<AIResponse id={self.id} risk_level={self.risk_level}>"
    
    def to_dict(self) -> dict:
        """Convert AI response to dictionary."""
        return {
            'id': self.id,
            'chat_session_id': self.chat_session_id,
            'user_message_id': self.user_message_id,
            'ai_message_id': self.ai_message_id,
            'model_used': self.model_used,
            'confidence': self.confidence,
            'risk_level': self.risk_level,
            'action_recommended': self.action_recommended,
            'generated_at': self.generated_at.isoformat() if self.generated_at else None,
            'response_time_ms': self.response_time_ms
        }
