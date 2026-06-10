"""
Database ORM Models for TALK 2 ME Mental Health Support System
Using SQLAlchemy for database abstraction
"""

from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Text, Float, DateTime, Boolean, 
    Enum, ForeignKey, JSON, DECIMAL, CheckConstraint, UniqueConstraint,
    Index, Date
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

Base = declarative_base()


# ============================================================================
# ENUMS
# ============================================================================

class GenderEnum(enum.Enum):
    Male = "Male"
    Female = "Female"
    Other = "Other"
    PreferNotToSay = "Prefer not to say"


class AccountTypeEnum(enum.Enum):
    User = "User"
    Counsellor = "Counsellor"
    Admin = "Admin"


class RiskLevelEnum(enum.Enum):
    Low = "Low"
    Moderate = "Moderate"
    High = "High"
    Severe = "Severe"


class ConversationTypeEnum(enum.Enum):
    UserAI = "User-AI"
    UserCounsellor = "User-Counsellor"
    Group = "Group"


class MessageTypeEnum(enum.Enum):
    Text = "Text"
    Image = "Image"
    Audio = "Audio"
    File = "File"
    Emoji = "Emoji"


class SentimentEnum(enum.Enum):
    Positive = "Positive"
    Neutral = "Neutral"
    Negative = "Negative"


class AlertTypeEnum(enum.Enum):
    KeywordDetection = "Keyword Detection"
    ManualReport = "Manual Report"
    PatternDetection = "Pattern Detection"


class SeverityEnum(enum.Enum):
    Low = "Low"
    Medium = "Medium"
    High = "High"
    Critical = "Critical"


class StatusEnum(enum.Enum):
    Active = "Active"
    Closed = "Closed"
    Archived = "Archived"


class PaymentStatusEnum(enum.Enum):
    Pending = "Pending"
    Paid = "Paid"
    Refunded = "Refunded"


class SessionStatusEnum(enum.Enum):
    Scheduled = "Scheduled"
    InProgress = "In Progress"
    Completed = "Completed"
    Cancelled = "Cancelled"
    NoShow = "No-show"


class PlanTypeEnum(enum.Enum):
    Free = "Free"
    Basic = "Basic"
    Professional = "Professional"
    Premium = "Premium"


# ============================================================================
# 1. USER MANAGEMENT MODELS
# ============================================================================

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(255))
    last_name = Column(String(255))
    phone_number = Column(String(20))
    date_of_birth = Column(Date)
    gender = Column(Enum(GenderEnum))
    language_preference = Column(String(50), default='en')
    account_type = Column(Enum(AccountTypeEnum), default=AccountTypeEnum.User)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime)

    # Relationships
    profile = relationship("UserProfile", uselist=False, back_populates="user", cascade="all, delete-orphan")
    assessments = relationship("Assessment", back_populates="user", cascade="all, delete-orphan")
    chat_conversations = relationship("ChatConversation", back_populates="user", cascade="all, delete-orphan")
    counselling_sessions = relationship("CounsellingSession", back_populates="user", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="user", cascade="all, delete-orphan")
    subscriptions = relationship("Subscription", back_populates="user", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    feedback = relationship("UserFeedback", foreign_keys="UserFeedback.user_id", cascade="all, delete-orphan")
    support_tickets = relationship("SupportTicket", back_populates="user", cascade="all, delete-orphan")
    crisis_alerts = relationship("CrisisAlert", back_populates="user", cascade="all, delete-orphan")

    __table_args__ = (
        Index('idx_email', 'email'),
        Index('idx_username', 'username'),
        Index('idx_account_type', 'account_type'),
    )


class UserProfile(Base):
    __tablename__ = 'user_profiles'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), unique=True, nullable=False)
    bio = Column(Text)
    profile_picture_url = Column(String(500))
    country = Column(String(100))
    region = Column(String(100))
    emergency_contact_name = Column(String(255))
    emergency_contact_phone = Column(String(20))
    insurance_provider = Column(String(255))
    insurance_policy_number = Column(String(255))
    medical_history = Column(Text)
    medications = Column(Text)
    allergies = Column(Text)
    preferred_communication = Column(String(50), default='Chat')
    notifications_enabled = Column(Boolean, default=True)
    marketing_emails_enabled = Column(Boolean, default=False)
    privacy_level = Column(String(50), default='Private')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="profile")

    __table_args__ = (
        Index('idx_user_id', 'user_id'),
    )


class Counsellor(Base):
    __tablename__ = 'counsellors'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), unique=True, nullable=False)
    license_number = Column(String(255), unique=True, nullable=False)
    specializations = Column(Text)  # JSON or comma-separated
    qualifications = Column(Text)
    experience_years = Column(Integer)
    bio = Column(Text)
    hourly_rate = Column(DECIMAL(10, 2))
    availability_status = Column(String(50), default='Offline')
    is_verified = Column(Boolean, default=False)
    verification_date = Column(DateTime)
    rating = Column(DECIMAL(3, 2), default=0)
    total_sessions = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    sessions = relationship("CounsellingSession", back_populates="counsellor", cascade="all, delete-orphan")
    chat_conversations = relationship("ChatConversation", back_populates="counsellor")

    __table_args__ = (
        Index('idx_user_id', 'user_id'),
        Index('idx_availability_status', 'availability_status'),
    )


# ============================================================================
# 2. AUTHENTICATION & SECURITY MODELS
# ============================================================================

class PasswordResetToken(Base):
    __tablename__ = 'password_reset_tokens'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    token = Column(String(500), unique=True, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    used = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index('idx_user_id', 'user_id'),
        Index('idx_token', 'token'),
    )


class EmailVerificationToken(Base):
    __tablename__ = 'email_verification_tokens'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    token = Column(String(500), unique=True, nullable=False)
    expires_at = Column(DateTime, nullable=False)
    verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index('idx_user_id', 'user_id'),
    )


class LoginHistory(Base):
    __tablename__ = 'login_history'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    ip_address = Column(String(45))
    user_agent = Column(Text)
    login_time = Column(DateTime, default=datetime.utcnow)
    logout_time = Column(DateTime)
    device_type = Column(String(50))

    __table_args__ = (
        Index('idx_user_id', 'user_id'),
        Index('idx_login_time', 'login_time'),
    )


# ============================================================================
# 3. ASSESSMENT MODELS
# ============================================================================

class AssessmentType(Base):
    __tablename__ = 'assessment_types'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    acronym = Column(String(50), unique=True)
    description = Column(Text)
    total_questions = Column(Integer)
    min_score = Column(Integer)
    max_score = Column(Integer)
    language = Column(String(50), default='en')
    created_at = Column(DateTime, default=datetime.utcnow)

    assessments = relationship("Assessment", back_populates="assessment_type")
    progress_trackers = relationship("AssessmentProgress", back_populates="assessment_type")

    __table_args__ = (
        Index('idx_acronym', 'acronym'),
    )


class Assessment(Base):
    __tablename__ = 'assessments'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    assessment_type_id = Column(Integer, ForeignKey('assessment_types.id', ondelete='CASCADE'), nullable=False)
    responses = Column(JSON)
    total_score = Column(Integer)
    risk_level = Column(Enum(RiskLevelEnum), default=RiskLevelEnum.Low)
    interpretation = Column(Text)
    recommendations = Column(Text)
    completed_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="assessments")
    assessment_type = relationship("AssessmentType", back_populates="assessments")

    __table_args__ = (
        Index('idx_user_id', 'user_id'),
        Index('idx_assessment_type_id', 'assessment_type_id'),
        Index('idx_completed_at', 'completed_at'),
        Index('idx_risk_level', 'risk_level'),
    )


class AssessmentProgress(Base):
    __tablename__ = 'assessment_progress'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    assessment_type_id = Column(Integer, ForeignKey('assessment_types.id', ondelete='CASCADE'), nullable=False)
    previous_score = Column(Integer)
    current_score = Column(Integer)
    score_change = Column(Integer)
    improvement_percentage = Column(DECIMAL(5, 2))
    days_since_last_assessment = Column(Integer)
    trend = Column(String(50))
    tracked_at = Column(DateTime, default=datetime.utcnow)

    assessment_type = relationship("AssessmentType", back_populates="progress_trackers")

    __table_args__ = (
        Index('idx_user_id', 'user_id'),
    )


# ============================================================================
# 4. CHAT & MESSAGING MODELS
# ============================================================================

class ChatConversation(Base):
    __tablename__ = 'chat_conversations'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    counsellor_id = Column(Integer, ForeignKey('counsellors.id', ondelete='SET NULL'))
    conversation_type = Column(Enum(ConversationTypeEnum), default=ConversationTypeEnum.UserAI)
    title = Column(String(255))
    status = Column(Enum(StatusEnum), default=StatusEnum.Active)
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime)
    total_messages = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="chat_conversations")
    counsellor = relationship("Counsellor", back_populates="chat_conversations")
    messages = relationship("ChatMessage", back_populates="conversation", cascade="all, delete-orphan")

    __table_args__ = (
        Index('idx_user_id', 'user_id'),
        Index('idx_status', 'status'),
        Index('idx_started_at', 'started_at'),
    )


class ChatMessage(Base):
    __tablename__ = 'chat_messages'

    id = Column(Integer, primary_key=True)
    conversation_id = Column(Integer, ForeignKey('chat_conversations.id', ondelete='CASCADE'), nullable=False)
    sender_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    sender_type = Column(String(50), default='User')
    message_text = Column(Text, nullable=False)
    message_type = Column(Enum(MessageTypeEnum), default=MessageTypeEnum.Text)
    file_url = Column(String(500))
    is_read = Column(Boolean, default=False)
    read_at = Column(DateTime)
    sentiment_score = Column(DECIMAL(3, 2))
    sentiment_label = Column(Enum(SentimentEnum))
    crisis_detected = Column(Boolean, default=False)
    crisis_keywords = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

    conversation = relationship("ChatConversation", back_populates="messages")
    sender = relationship("User")
    reactions = relationship("MessageReaction", back_populates="message", cascade="all, delete-orphan")

    __table_args__ = (
        Index('idx_conversation_id', 'conversation_id'),
        Index('idx_sender_id', 'sender_id'),
        Index('idx_created_at', 'created_at'),
        Index('idx_crisis_detected', 'crisis_detected'),
    )


class MessageReaction(Base):
    __tablename__ = 'message_reactions'

    id = Column(Integer, primary_key=True)
    message_id = Column(Integer, ForeignKey('chat_messages.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    reaction_emoji = Column(String(10))
    created_at = Column(DateTime, default=datetime.utcnow)

    message = relationship("ChatMessage", back_populates="reactions")

    __table_args__ = (
        Index('idx_message_id', 'message_id'),
        UniqueConstraint('message_id', 'user_id', name='unique_reaction'),
    )


# ============================================================================
# 5. CRISIS MANAGEMENT MODELS
# ============================================================================

class CrisisAlert(Base):
    __tablename__ = 'crisis_alerts'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    message_id = Column(Integer, ForeignKey('chat_messages.id', ondelete='SET NULL'))
    alert_type = Column(Enum(AlertTypeEnum), default=AlertTypeEnum.KeywordDetection)
    severity = Column(Enum(SeverityEnum), default=SeverityEnum.High)
    keywords_detected = Column(JSON)
    description = Column(Text)
    status = Column(String(50), default='Active')
    assigned_to = Column(Integer, ForeignKey('counsellors.id', ondelete='SET NULL'))
    reviewed_by = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'))
    action_taken = Column(Text)
    review_notes = Column(Text)
    resolved_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", foreign_keys=[user_id], back_populates="crisis_alerts")

    __table_args__ = (
        Index('idx_user_id', 'user_id'),
        Index('idx_severity', 'severity'),
        Index('idx_status', 'status'),
        Index('idx_created_at', 'created_at'),
    )


class EmergencyResource(Base):
    __tablename__ = 'emergency_resources'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    resource_type = Column(String(50), default='Hotline')
    contact_number = Column(String(20))
    email = Column(String(255))
    website_url = Column(String(500))
    address = Column(Text)
    country = Column(String(100))
    region = Column(String(100))
    available_24_7 = Column(Boolean, default=True)
    languages_supported = Column(JSON)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index('idx_country', 'country'),
        Index('idx_resource_type', 'resource_type'),
    )


# ============================================================================
# 6. COUNSELLING MODELS
# ============================================================================

class CounsellingSession(Base):
    __tablename__ = 'counselling_sessions'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    counsellor_id = Column(Integer, ForeignKey('counsellors.id', ondelete='CASCADE'), nullable=False)
    session_type = Column(String(50), default='Individual')
    communication_method = Column(String(50), default='Chat')
    scheduled_at = Column(DateTime)
    started_at = Column(DateTime)
    ended_at = Column(DateTime)
    duration_minutes = Column(Integer)
    status = Column(Enum(SessionStatusEnum), default=SessionStatusEnum.Scheduled)
    notes = Column(Text)
    session_plan = Column(Text)
    outcome = Column(Text)
    follow_up_required = Column(Boolean, default=False)
    follow_up_date = Column(DateTime)
    cost = Column(DECIMAL(10, 2))
    payment_status = Column(Enum(PaymentStatusEnum), default=PaymentStatusEnum.Pending)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="counselling_sessions")
    counsellor = relationship("Counsellor", back_populates="sessions")
    session_notes = relationship("SessionNotes", uselist=False, back_populates="session", cascade="all, delete-orphan")

    __table_args__ = (
        Index('idx_user_id', 'user_id'),
        Index('idx_counsellor_id', 'counsellor_id'),
        Index('idx_status', 'status'),
        Index('idx_scheduled_at', 'scheduled_at'),
    )


class SessionNotes(Base):
    __tablename__ = 'session_notes'

    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey('counselling_sessions.id', ondelete='CASCADE'), unique=True, nullable=False)
    clinical_notes = Column(Text)
    diagnosis_notes = Column(Text)
    treatment_plan = Column(Text)
    medications_prescribed = Column(Text)
    referrals = Column(Text)
    follow_up_instructions = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    session = relationship("CounsellingSession", back_populates="session_notes")


# ============================================================================
# 7. RESOURCES & CONTENT MODELS
# ============================================================================

class Resource(Base):
    __tablename__ = 'resources'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    content_type = Column(String(50), default='Article')
    content_url = Column(String(500))
    category = Column(String(100))
    subcategory = Column(String(100))
    tags = Column(JSON)
    language = Column(String(50), default='en')
    author = Column(String(255))
    source = Column(String(255))
    is_published = Column(Boolean, default=False)
    view_count = Column(Integer, default=0)
    rating = Column(DECIMAL(3, 2), default=0)
    difficulty_level = Column(String(50), default='Beginner')
    estimated_read_time_minutes = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    views = relationship("ResourceView", back_populates="resource", cascade="all, delete-orphan")
    ratings = relationship("ResourceRating", back_populates="resource", cascade="all, delete-orphan")

    __table_args__ = (
        Index('idx_category', 'category'),
        Index('idx_language', 'language'),
        Index('idx_is_published', 'is_published'),
    )


class ResourceView(Base):
    __tablename__ = 'resource_views'

    id = Column(Integer, primary_key=True)
    resource_id = Column(Integer, ForeignKey('resources.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'))
    viewed_at = Column(DateTime, default=datetime.utcnow)
    time_spent_seconds = Column(Integer)
    completed = Column(Boolean, default=False)

    resource = relationship("Resource", back_populates="views")

    __table_args__ = (
        Index('idx_resource_id', 'resource_id'),
        Index('idx_user_id', 'user_id'),
    )


class ResourceRating(Base):
    __tablename__ = 'resource_ratings'

    id = Column(Integer, primary_key=True)
    resource_id = Column(Integer, ForeignKey('resources.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    rating = Column(Integer, nullable=False)
    review_text = Column(Text)
    helpful_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    resource = relationship("Resource", back_populates="ratings")

    __table_args__ = (
        Index('idx_resource_id', 'resource_id'),
        UniqueConstraint('resource_id', 'user_id', name='unique_rating'),
        CheckConstraint('rating >= 1 AND rating <= 5', name='rating_range'),
    )


# ============================================================================
# 8. PAYMENT & SUBSCRIPTION MODELS
# ============================================================================

class Payment(Base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    transaction_type = Column(String(50), default='Session')
    amount = Column(DECIMAL(10, 2), nullable=False)
    currency = Column(String(3), default='USD')
    payment_method = Column(String(50), default='Credit Card')
    payment_gateway = Column(String(100))
    transaction_id = Column(String(255), unique=True)
    reference_id = Column(Integer)
    status = Column(String(50), default='Pending')
    error_message = Column(Text)
    receipt_url = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="payments")

    __table_args__ = (
        Index('idx_user_id', 'user_id'),
        Index('idx_status', 'status'),
        Index('idx_created_at', 'created_at'),
    )


class Subscription(Base):
    __tablename__ = 'subscriptions'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    plan_type = Column(Enum(PlanTypeEnum), default=PlanTypeEnum.Free)
    subscription_status = Column(String(50), default='Active')
    start_date = Column(Date)
    end_date = Column(Date)
    auto_renew = Column(Boolean, default=True)
    sessions_limit = Column(Integer)
    sessions_used = Column(Integer, default=0)
    storage_limit_gb = Column(Integer)
    storage_used_gb = Column(DECIMAL(10, 2), default=0)
    features = Column(JSON)
    price = Column(DECIMAL(10, 2))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="subscriptions")

    __table_args__ = (
        Index('idx_user_id', 'user_id'),
        Index('idx_subscription_status', 'subscription_status'),
    )


# ============================================================================
# 9. NOTIFICATION MODELS
# ============================================================================

class Notification(Base):
    __tablename__ = 'notifications'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    notification_type = Column(String(50), default='System')
    title = Column(String(255))
    message = Column(Text, nullable=False)
    related_id = Column(Integer)
    is_read = Column(Boolean, default=False)
    read_at = Column(DateTime)
    action_url = Column(String(500))
    priority = Column(String(50), default='Medium')
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="notifications")

    __table_args__ = (
        Index('idx_user_id', 'user_id'),
        Index('idx_is_read', 'is_read'),
        Index('idx_created_at', 'created_at'),
    )


class SMSLog(Base):
    __tablename__ = 'sms_log'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    phone_number = Column(String(20))
    message = Column(Text)
    status = Column(String(50), default='Pending')
    message_id = Column(String(255))
    error_message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    sent_at = Column(DateTime)

    __table_args__ = (
        Index('idx_user_id', 'user_id'),
    )


class EmailLog(Base):
    __tablename__ = 'email_log'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    email_address = Column(String(255))
    subject = Column(String(255))
    message_type = Column(String(100))
    status = Column(String(50), default='Pending')
    error_message = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    sent_at = Column(DateTime)

    __table_args__ = (
        Index('idx_user_id', 'user_id'),
        Index('idx_status', 'status'),
    )


# ============================================================================
# 10. ANALYTICS & REPORTING MODELS
# ============================================================================

class UserAnalytics(Base):
    __tablename__ = 'user_analytics'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    total_sessions = Column(Integer, default=0)
    total_messages = Column(Integer, default=0)
    assessments_completed = Column(Integer, default=0)
    resources_viewed = Column(Integer, default=0)
    average_sentiment_score = Column(DECIMAL(3, 2))
    crisis_incidents = Column(Integer, default=0)
    last_active_date = Column(DateTime)
    engagement_score = Column(DECIMAL(5, 2), default=0)
    tracked_date = Column(Date)

    __table_args__ = (
        Index('idx_user_id', 'user_id'),
        UniqueConstraint('user_id', 'tracked_date', name='unique_user_date'),
    )


class SystemAnalytics(Base):
    __tablename__ = 'system_analytics'

    id = Column(Integer, primary_key=True)
    tracked_date = Column(Date, unique=True, nullable=False)
    total_active_users = Column(Integer)
    new_users_today = Column(Integer)
    total_sessions_today = Column(Integer)
    total_messages_today = Column(Integer)
    crisis_alerts_today = Column(Integer)
    average_session_duration_minutes = Column(DECIMAL(10, 2))
    server_uptime_percentage = Column(DECIMAL(5, 2))
    error_count = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)


class AIModelPerformance(Base):
    __tablename__ = 'ai_model_performance'

    id = Column(Integer, primary_key=True)
    model_name = Column(String(255))
    model_version = Column(String(50))
    metric_type = Column(String(50), default='Accuracy')
    metric_value = Column(DECIMAL(5, 4))
    test_dataset_size = Column(Integer)
    tested_at = Column(DateTime)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index('idx_model_name', 'model_name'),
    )


# ============================================================================
# 11. ADMIN & MODERATION MODELS
# ============================================================================

class AdminActionsLog(Base):
    __tablename__ = 'admin_actions_log'

    id = Column(Integer, primary_key=True)
    admin_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    action_type = Column(String(100))
    entity_type = Column(String(100))
    entity_id = Column(Integer)
    old_value = Column(Text)
    new_value = Column(Text)
    reason = Column(Text)
    ip_address = Column(String(45))
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index('idx_admin_id', 'admin_id'),
        Index('idx_action_type', 'action_type'),
        Index('idx_created_at', 'created_at'),
    )


class ContentModeration(Base):
    __tablename__ = 'content_moderation'

    id = Column(Integer, primary_key=True)
    content_type = Column(String(50), default='Message')
    content_id = Column(Integer)
    reported_by = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'))
    reason = Column(String(50), default='Other')
    description = Column(Text)
    status = Column(String(50), default='Reported')
    reviewed_by = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'))
    moderation_note = Column(Text)
    action_taken = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    reviewed_at = Column(DateTime)

    __table_args__ = (
        Index('idx_status', 'status'),
        Index('idx_created_at', 'created_at'),
    )


class UserReport(Base):
    __tablename__ = 'user_reports'

    id = Column(Integer, primary_key=True)
    reported_user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    reported_by = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    report_type = Column(String(50), default='Other')
    description = Column(Text)
    status = Column(String(50), default='Reported')
    action_taken = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index('idx_reported_user_id', 'reported_user_id'),
        Index('idx_status', 'status'),
    )


# ============================================================================
# 12. SYSTEM CONFIGURATION MODELS
# ============================================================================

class SystemSetting(Base):
    __tablename__ = 'system_settings'

    id = Column(Integer, primary_key=True)
    setting_key = Column(String(255), unique=True, nullable=False)
    setting_value = Column(Text)
    description = Column(Text)
    data_type = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index('idx_setting_key', 'setting_key'),
    )


class FeatureFlag(Base):
    __tablename__ = 'feature_flags'

    id = Column(Integer, primary_key=True)
    flag_name = Column(String(255), unique=True, nullable=False)
    is_enabled = Column(Boolean, default=False)
    description = Column(Text)
    rollout_percentage = Column(Integer, default=100)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index('idx_flag_name', 'flag_name'),
    )


# ============================================================================
# 13. AUDIT TRAIL MODELS
# ============================================================================

class AuditTrail(Base):
    __tablename__ = 'audit_trail'

    id = Column(Integer, primary_key=True)
    table_name = Column(String(100))
    record_id = Column(Integer)
    operation = Column(String(50), nullable=False)
    old_data = Column(JSON)
    new_data = Column(JSON)
    changed_by = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'))
    change_reason = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index('idx_table_name', 'table_name'),
        Index('idx_created_at', 'created_at'),
    )


class DataRetentionPolicy(Base):
    __tablename__ = 'data_retention_policies'

    id = Column(Integer, primary_key=True)
    table_name = Column(String(100))
    retention_days = Column(Integer)
    auto_delete = Column(Boolean, default=False)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# ============================================================================
# 14. SUPPORT & FEEDBACK MODELS
# ============================================================================

class UserFeedback(Base):
    __tablename__ = 'user_feedback'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'))
    feedback_type = Column(String(50), default='General Feedback')
    category = Column(String(100))
    subject = Column(String(255))
    message = Column(Text, nullable=False)
    attachment_url = Column(String(500))
    status = Column(String(50), default='New')
    response = Column(Text)
    responded_by = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'))
    rating = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index('idx_status', 'status'),
        Index('idx_created_at', 'created_at'),
    )


class SupportTicket(Base):
    __tablename__ = 'support_tickets'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    ticket_number = Column(String(50), unique=True, nullable=False)
    subject = Column(String(255), nullable=False)
    description = Column(Text)
    category = Column(String(100))
    priority = Column(String(50), default='Medium')
    status = Column(String(50), default='Open')
    assigned_to = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'))
    resolution = Column(Text)
    resolved_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="support_tickets")
    responses = relationship("SupportTicketResponse", back_populates="ticket", cascade="all, delete-orphan")

    __table_args__ = (
        Index('idx_user_id', 'user_id'),
        Index('idx_status', 'status'),
        Index('idx_priority', 'priority'),
    )


class SupportTicketResponse(Base):
    __tablename__ = 'support_ticket_responses'

    id = Column(Integer, primary_key=True)
    ticket_id = Column(Integer, ForeignKey('support_tickets.id', ondelete='CASCADE'), nullable=False)
    responder_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    response_text = Column(Text, nullable=False)
    attachment_url = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)

    ticket = relationship("SupportTicket", back_populates="responses")

    __table_args__ = (
        Index('idx_ticket_id', 'ticket_id'),
    )


# ============================================================================
# 15. TRANSLATION & LOCALIZATION MODELS
# ============================================================================

class SupportedLanguage(Base):
    __tablename__ = 'supported_languages'

    id = Column(Integer, primary_key=True)
    language_code = Column(String(10), unique=True, nullable=False)
    language_name = Column(String(100), nullable=False)
    native_name = Column(String(100))
    is_active = Column(Boolean, default=True)
    native_speakers = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

    translations = relationship("Translation", back_populates="language")


class Translation(Base):
    __tablename__ = 'translations'

    id = Column(Integer, primary_key=True)
    language_code = Column(String(10), ForeignKey('supported_languages.language_code', ondelete='CASCADE'), nullable=False)
    translation_key = Column(String(255), nullable=False)
    translation_value = Column(Text, nullable=False)
    context = Column(String(100))
    translator_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'))
    is_reviewed = Column(Boolean, default=False)
    reviewed_by = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    language = relationship("SupportedLanguage", back_populates="translations")

    __table_args__ = (
        UniqueConstraint('language_code', 'translation_key', name='unique_translation'),
        Index('idx_language_code', 'language_code'),
    )
