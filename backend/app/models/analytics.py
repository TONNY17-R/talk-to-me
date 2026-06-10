"""
Analytics models for Talk to Me platform.

This module contains models for tracking user engagement and platform analytics.
"""

from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Text, JSON
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class UserAnalytics:
    """
    Represents analytics data for individual users.
    
    Attributes:
        id: Unique identifier for the analytics record
        user_id: Foreign key to the User
        total_sessions: Total number of chat sessions
        total_messages: Total number of messages sent
        average_session_duration: Average duration of sessions in minutes
        messages_per_day: Average messages per day
        last_activity: Last time user was active
        most_discussed_topics: JSON array of most discussed topics
        sentiment_trend: JSON array of sentiment scores over time
        platform_usage_hours: Total hours spent on platform
        feature_usage: JSON object of feature usage counts
        risk_alerts_triggered: Number of times risk alerts were triggered
        created_at: When the analytics record was created
        updated_at: When the analytics was last updated
    """
    __tablename__ = 'user_analytics'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, unique=True)
    total_sessions = Column(Integer, default=0)
    total_messages = Column(Integer, default=0)
    average_session_duration = Column(Float, default=0.0)
    messages_per_day = Column(Float, default=0.0)
    last_activity = Column(DateTime, nullable=True)
    most_discussed_topics = Column(JSON, nullable=True)  # Array of topic strings
    sentiment_trend = Column(JSON, nullable=True)  # Array of sentiment scores
    platform_usage_hours = Column(Float, default=0.0)
    feature_usage = Column(JSON, nullable=True)  # Object with feature usage counts
    risk_alerts_triggered = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship('User', backref='analytics', uselist=False)
    
    def __repr__(self) -> str:
        return f"<UserAnalytics id={self.id} user_id={self.user_id}>"
    
    def to_dict(self) -> dict:
        """Convert analytics to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'total_sessions': self.total_sessions,
            'total_messages': self.total_messages,
            'average_session_duration': self.average_session_duration,
            'messages_per_day': self.messages_per_day,
            'last_activity': self.last_activity.isoformat() if self.last_activity else None,
            'most_discussed_topics': self.most_discussed_topics,
            'sentiment_trend': self.sentiment_trend,
            'platform_usage_hours': self.platform_usage_hours,
            'risk_alerts_triggered': self.risk_alerts_triggered,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class PlatformAnalytics:
    """
    Represents overall platform-wide analytics.
    
    Attributes:
        id: Unique identifier for the analytics record
        date: Date of the analytics record
        total_active_users: Total active users on this date
        new_users_count: New users registered on this date
        total_sessions: Total sessions on this date
        total_messages: Total messages exchanged on this date
        average_sentiment: Average sentiment of messages
        critical_risk_alerts: Number of critical risk alerts
        high_risk_alerts: Number of high risk alerts
        platform_uptime_percentage: Platform uptime %
        average_response_time_ms: Average AI response time
        user_satisfaction_score: Average user satisfaction rating
        most_active_hour: Most active hour of the day
        metadata: Additional metadata/notes
        created_at: When the record was created
    """
    __tablename__ = 'platform_analytics'
    
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, default=datetime.utcnow, unique=True)
    total_active_users = Column(Integer, default=0)
    new_users_count = Column(Integer, default=0)
    total_sessions = Column(Integer, default=0)
    total_messages = Column(Integer, default=0)
    average_sentiment = Column(Float, default=0.0)
    critical_risk_alerts = Column(Integer, default=0)
    high_risk_alerts = Column(Integer, default=0)
    platform_uptime_percentage = Column(Float, default=100.0)
    average_response_time_ms = Column(Float, default=0.0)
    user_satisfaction_score = Column(Float, default=0.0)
    most_active_hour = Column(Integer, nullable=True)  # 0-23
    metadata = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"<PlatformAnalytics date={self.date} active_users={self.total_active_users}>"
    
    def to_dict(self) -> dict:
        """Convert analytics to dictionary."""
        return {
            'id': self.id,
            'date': self.date.isoformat() if self.date else None,
            'total_active_users': self.total_active_users,
            'new_users_count': self.new_users_count,
            'total_sessions': self.total_sessions,
            'total_messages': self.total_messages,
            'average_sentiment': self.average_sentiment,
            'critical_risk_alerts': self.critical_risk_alerts,
            'high_risk_alerts': self.high_risk_alerts,
            'platform_uptime_percentage': self.platform_uptime_percentage,
            'average_response_time_ms': self.average_response_time_ms,
            'user_satisfaction_score': self.user_satisfaction_score,
            'most_active_hour': self.most_active_hour
        }


class CrisisAlert:
    """
    Represents a crisis alert for a user.
    
    Attributes:
        id: Unique identifier for the alert
        user_id: Foreign key to the User
        alert_type: Type of crisis (suicide_risk, self_harm, substance_abuse, etc.)
        risk_level: Severity level (critical, high, medium)
        trigger_message: The message that triggered the alert
        description: Description of the alert
        action_taken: Actions taken in response to the alert
        emergency_contact_notified: Whether emergency contact was notified
        professional_notified: Whether a mental health professional was notified
        resolved_at: When the crisis was resolved
        resolution_notes: Notes on how it was resolved
        created_at: When the alert was created
        updated_at: When the alert was last updated
    """
    __tablename__ = 'crisis_alerts'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    alert_type = Column(String(100), nullable=False)
    risk_level = Column(String(20), nullable=False)  # critical, high, medium
    trigger_message = Column(Text, nullable=True)
    description = Column(Text, nullable=False)
    action_taken = Column(Text, nullable=True)
    emergency_contact_notified = Column(String(50), nullable=True)  # Email or phone
    professional_notified = Column(String(50), nullable=True)  # Email or phone
    resolved_at = Column(DateTime, nullable=True)
    resolution_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship('User', backref='crisis_alerts')
    
    def __repr__(self) -> str:
        return f"<CrisisAlert id={self.id} user_id={self.user_id} risk_level={self.risk_level}>"
    
    def to_dict(self) -> dict:
        """Convert crisis alert to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'alert_type': self.alert_type,
            'risk_level': self.risk_level,
            'trigger_message': self.trigger_message,
            'description': self.description,
            'action_taken': self.action_taken,
            'emergency_contact_notified': self.emergency_contact_notified,
            'professional_notified': self.professional_notified,
            'resolved_at': self.resolved_at.isoformat() if self.resolved_at else None,
            'resolution_notes': self.resolution_notes,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
