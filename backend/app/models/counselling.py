"""
Counselling models for Talk to Me platform.

This module contains models for managing counselling appointments and sessions.
"""

from datetime import datetime
from enum import Enum

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SQLEnum, Float, Boolean
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class AppointmentStatus(str, Enum):
    """Enum for appointment statuses."""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"
    RESCHEDULED = "rescheduled"


class SessionModality(str, Enum):
    """Enum for counselling session modalities."""
    VIDEO = "video"
    VOICE = "voice"
    CHAT = "chat"
    IN_PERSON = "in_person"


class Appointment:
    """
    Represents a counselling appointment between a user and counselor.
    
    Attributes:
        id: Unique identifier for the appointment
        user_id: Foreign key to the User
        counselor_id: Foreign key to the Counselor (User with counselor profile)
        scheduled_date: Date and time of the appointment
        duration_minutes: Expected duration of the appointment
        status: Current status of the appointment
        modality: How the session will be conducted
        notes: Any special notes for the appointment
        created_at: When the appointment was created
        created_by: Who created the appointment
    """
    __tablename__ = 'appointments'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    counselor_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    scheduled_date = Column(DateTime, nullable=False)
    duration_minutes = Column(Integer, default=60)
    status = Column(SQLEnum(AppointmentStatus), default=AppointmentStatus.PENDING)
    modality = Column(SQLEnum(SessionModality), default=SessionModality.VIDEO)
    notes = Column(Text, nullable=True)
    reminder_sent = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship('User', foreign_keys=[user_id], backref='appointments')
    counselor = relationship('User', foreign_keys=[counselor_id], backref='conducted_appointments')
    session = relationship('CounsellingSession', uselist=False, back_populates='appointment')
    
    def __repr__(self) -> str:
        return f"<Appointment id={self.id} user_id={self.user_id} counselor_id={self.counselor_id}>"
    
    def to_dict(self) -> dict:
        """Convert appointment to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'counselor_id': self.counselor_id,
            'scheduled_date': self.scheduled_date.isoformat() if self.scheduled_date else None,
            'duration_minutes': self.duration_minutes,
            'status': self.status.value if self.status else None,
            'modality': self.modality.value if self.modality else None,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class CounsellingSession:
    """
    Represents an actual counselling session between user and counselor.
    
    Attributes:
        id: Unique identifier for the session
        appointment_id: Foreign key to the Appointment
        started_at: When the session actually started
        ended_at: When the session ended
        duration_actual_minutes: Actual duration of the session
        session_notes: Notes from the counselor about the session
        topics_discussed: Main topics discussed
        follow_up_actions: Recommended follow-up actions
        is_completed: Whether the session was completed
    """
    __tablename__ = 'counselling_sessions'
    
    id = Column(Integer, primary_key=True)
    appointment_id = Column(Integer, ForeignKey('appointments.id'), nullable=False)
    started_at = Column(DateTime, nullable=True)
    ended_at = Column(DateTime, nullable=True)
    duration_actual_minutes = Column(Integer, nullable=True)
    session_notes = Column(Text, nullable=True)
    topics_discussed = Column(Text, nullable=True)
    follow_up_actions = Column(Text, nullable=True)
    is_completed = Column(Boolean, default=False)
    session_recording_url = Column(String(500), nullable=True)  # URL to session recording
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    appointment = relationship('Appointment', back_populates='session')
    reviews = relationship('CounsellorReview', back_populates='session', cascade='all, delete-orphan')
    
    def __repr__(self) -> str:
        return f"<CounsellingSession id={self.id} appointment_id={self.appointment_id}>"
    
    def to_dict(self) -> dict:
        """Convert session to dictionary."""
        return {
            'id': self.id,
            'appointment_id': self.appointment_id,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'ended_at': self.ended_at.isoformat() if self.ended_at else None,
            'duration_actual_minutes': self.duration_actual_minutes,
            'session_notes': self.session_notes,
            'topics_discussed': self.topics_discussed,
            'follow_up_actions': self.follow_up_actions,
            'is_completed': self.is_completed,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class CounsellorReview:
    """
    Represents a review/feedback of a counselling session.
    
    Attributes:
        id: Unique identifier for the review
        session_id: Foreign key to the CounsellingSession
        reviewer_id: Foreign key to the reviewer (user who reviewed)
        rating: Rating of the session (1-5 stars)
        feedback: Detailed feedback
        professionalism_score: Rating of counselor professionalism
        effectiveness_score: Rating of session effectiveness
        would_recommend: Would the user recommend this counselor
        created_at: When the review was created
    """
    __tablename__ = 'counsellor_reviews'
    
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey('counselling_sessions.id'), nullable=False)
    reviewer_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    rating = Column(Float, nullable=False)  # 1-5 stars
    feedback = Column(Text, nullable=True)
    professionalism_score = Column(Float, nullable=True)  # 1-5
    effectiveness_score = Column(Float, nullable=True)  # 1-5
    would_recommend = Column(Boolean, default=True)
    is_anonymous = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    session = relationship('CounsellingSession', back_populates='reviews')
    reviewer = relationship('User', backref='session_reviews')
    
    def __repr__(self) -> str:
        return f"<CounsellorReview id={self.id} session_id={self.session_id} rating={self.rating}>"
    
    def to_dict(self) -> dict:
        """Convert review to dictionary."""
        return {
            'id': self.id,
            'session_id': self.session_id,
            'reviewer_id': self.reviewer_id,
            'rating': self.rating,
            'feedback': self.feedback,
            'professionalism_score': self.professionalism_score,
            'effectiveness_score': self.effectiveness_score,
            'would_recommend': self.would_recommend,
            'is_anonymous': self.is_anonymous,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
