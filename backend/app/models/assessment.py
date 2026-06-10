"""
Assessment models for Talk to Me platform.

This module contains models for managing mental health assessments and evaluations.
"""

from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SQLEnum, Float, Boolean, JSON
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class AssessmentType(str, Enum):
    """Enum for different types of assessments."""
    PHQ9 = "phq9"  # Patient Health Questionnaire-9 (Depression)
    GAD7 = "gad7"  # Generalized Anxiety Disorder-7
    DASS21 = "dass21"  # Depression Anxiety Stress Scale
    PCPTSD = "pc_ptsd"  # Primary Care PTSD Screen
    PSQI = "psqi"  # Pittsburgh Sleep Quality Index
    GENERAL = "general"  # General mental health screening


class RiskLevel(str, Enum):
    """Enum for risk assessment levels."""
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"


class Assessment:
    """
    Represents a mental health assessment session.
    
    Attributes:
        id: Unique identifier for the assessment
        user_id: Foreign key to the User
        assessment_type: Type of assessment conducted
        started_at: When the assessment started
        completed_at: When the assessment was completed
        is_completed: Whether the assessment is complete
        overall_score: Total score for the assessment
        risk_level: Assessed risk level
        recommendations: Recommended interventions
        notes: Additional clinical notes
    """
    __tablename__ = 'assessments'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    assessment_type = Column(SQLEnum(AssessmentType), nullable=False)
    started_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    is_completed = Column(Boolean, default=False)
    overall_score = Column(Float, nullable=True)
    risk_level = Column(SQLEnum(RiskLevel), nullable=True)
    recommendations = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    reviewed_by = Column(Integer, ForeignKey('users.id'), nullable=True)  # Counselor review
    
    # Relationships
    user = relationship('User', foreign_keys=[user_id], backref='assessments')
    counselor = relationship('User', foreign_keys=[reviewed_by])
    questions = relationship('AssessmentQuestion', back_populates='assessment', cascade='all, delete-orphan')
    responses = relationship('AssessmentResponse', back_populates='assessment', cascade='all, delete-orphan')
    
    def __repr__(self) -> str:
        return f"<Assessment id={self.id} type={self.assessment_type} user_id={self.user_id}>"
    
    def to_dict(self) -> dict:
        """Convert assessment to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'assessment_type': self.assessment_type.value if self.assessment_type else None,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'is_completed': self.is_completed,
            'overall_score': self.overall_score,
            'risk_level': self.risk_level.value if self.risk_level else None,
            'recommendations': self.recommendations,
            'notes': self.notes
        }


class AssessmentQuestion:
    """
    Represents a single question in an assessment.
    
    Attributes:
        id: Unique identifier for the question
        assessment_id: Foreign key to the Assessment
        question_number: Order of the question
        question_text: The actual question
        question_type: Type of question (multiple choice, scale, yes/no, etc.)
        options: Possible answer options
        score_mapping: How answers map to scores
    """
    __tablename__ = 'assessment_questions'
    
    id = Column(Integer, primary_key=True)
    assessment_id = Column(Integer, ForeignKey('assessments.id'), nullable=False)
    question_number = Column(Integer, nullable=False)
    question_text = Column(Text, nullable=False)
    question_type = Column(String(50), nullable=False)  # 'multiple_choice', 'scale', 'yes_no', 'text'
    options = Column(JSON, nullable=True)  # JSON array of options
    score_mapping = Column(JSON, nullable=True)  # JSON mapping of options to scores
    is_required = Column(Boolean, default=True)
    
    # Relationships
    assessment = relationship('Assessment', back_populates='questions')
    responses = relationship('AssessmentResponse', back_populates='question', cascade='all, delete-orphan')
    
    def __repr__(self) -> str:
        return f"<AssessmentQuestion id={self.id} assessment_id={self.assessment_id}>"
    
    def to_dict(self) -> dict:
        """Convert question to dictionary."""
        return {
            'id': self.id,
            'assessment_id': self.assessment_id,
            'question_number': self.question_number,
            'question_text': self.question_text,
            'question_type': self.question_type,
            'options': self.options,
            'is_required': self.is_required
        }


class AssessmentResponse:
    """
    Represents a user's answer to an assessment question.
    
    Attributes:
        id: Unique identifier for the response
        assessment_id: Foreign key to the Assessment
        question_id: Foreign key to the AssessmentQuestion
        answer: The user's answer
        score: Score value for this answer
        answered_at: When the answer was provided
    """
    __tablename__ = 'assessment_responses'
    
    id = Column(Integer, primary_key=True)
    assessment_id = Column(Integer, ForeignKey('assessments.id'), nullable=False)
    question_id = Column(Integer, ForeignKey('assessment_questions.id'), nullable=False)
    answer = Column(Text, nullable=False)  # Can store multiple data types as text
    score = Column(Float, nullable=True)
    answered_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    time_spent_seconds = Column(Integer, nullable=True)  # Time spent on this question
    
    # Relationships
    assessment = relationship('Assessment', back_populates='responses')
    question = relationship('AssessmentQuestion', back_populates='responses')
    
    def __repr__(self) -> str:
        return f"<AssessmentResponse id={self.id} question_id={self.question_id}>"
    
    def to_dict(self) -> dict:
        """Convert response to dictionary."""
        return {
            'id': self.id,
            'assessment_id': self.assessment_id,
            'question_id': self.question_id,
            'answer': self.answer,
            'score': self.score,
            'answered_at': self.answered_at.isoformat() if self.answered_at else None,
            'time_spent_seconds': self.time_spent_seconds
        }
