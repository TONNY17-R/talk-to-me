from app import db
from datetime import datetime
import uuid
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(15), unique=True, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    
    # Personal Information
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(20))
    location = db.Column(db.String(100))
    district = db.Column(db.String(50))
    language = db.Column(db.String(10), default='en')
    
    # Mental Health Profile
    current_mood = db.Column(db.String(20), default='neutral')
    last_assessment_score = db.Column(db.Float)
    risk_level = db.Column(db.String(20), default='low')
    
    # Account Settings
    is_anonymous = db.Column(db.Boolean, default=True)
    is_counsellor = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_verified = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    
    # Subscription
    subscription_tier = db.Column(db.String(20), default='free')
    subscription_end = db.Column(db.DateTime)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    last_activity = db.Column(db.DateTime)
    
    # Relationships
    sessions = db.relationship('UserSession', backref='user', lazy=True, cascade='all, delete-orphan')
    assessments = db.relationship('Assessment', backref='user', lazy=True)
    appointments = db.relationship('Appointment', backref='user', lazy=True)
    chats = db.relationship('ChatSession', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self, include_sensitive=False):
        data = {
            'id': self.id,
            'username': self.username,
            'email': self.email if include_sensitive else None,
            'phone': self.phone if include_sensitive else None,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'age': self.age,
            'gender': self.gender,
            'location': self.location,
            'district': self.district,
            'language': self.language,
            'current_mood': self.current_mood,
            'risk_level': self.risk_level,
            'is_anonymous': self.is_anonymous,
            'is_counsellor': self.is_counsellor,
            'is_verified': self.is_verified,
            'subscription_tier': self.subscription_tier,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }
        
        if include_sensitive:
            data['email'] = self.email
            data['phone'] = self.phone
            
        return data
    
    def update_activity(self):
        self.last_activity = datetime.utcnow()
        db.session.commit()

class CounsellorProfile(db.Model):
    __tablename__ = 'counsellor_profiles'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), unique=True, nullable=False)
    
    # Professional Information
    qualification = db.Column(db.String(200))
    specialization = db.Column(db.String(200))
    license_number = db.Column(db.String(50))
    years_experience = db.Column(db.Integer)
    
    # Availability
    availability_schedule = db.Column(db.JSON)  # JSON structure for weekly schedule
    session_duration = db.Column(db.Integer, default=60)  # minutes
    session_price = db.Column(db.Float, default=0.0)
    
    # Ratings
    average_rating = db.Column(db.Float, default=0.0)
    total_sessions = db.Column(db.Integer, default=0)
    
    # Languages spoken
    languages = db.Column(db.JSON, default=['en'])  # List of languages
    
    # Bio
    bio = db.Column(db.Text)
    profile_image = db.Column(db.String(255))
    
    # Verification
    is_verified = db.Column(db.Boolean, default=False)
    verification_documents = db.Column(db.JSON)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    user = db.relationship('User', backref='counsellor_profile', uselist=False)
    appointments = db.relationship('Appointment', backref='counsellor', lazy=True)
    reviews = db.relationship('CounsellorReview', backref='counsellor', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'qualification': self.qualification,
            'specialization': self.specialization,
            'license_number': self.license_number,
            'years_experience': self.years_experience,
            'availability_schedule': self.availability_schedule,
            'session_duration': self.session_duration,
            'session_price': self.session_price,
            'average_rating': self.average_rating,
            'total_sessions': self.total_sessions,
            'languages': self.languages,
            'bio': self.bio,
            'profile_image': self.profile_image,
            'is_verified': self.is_verified,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class UserSession(db.Model):
    __tablename__ = 'user_sessions'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    session_token = db.Column(db.String(255), unique=True, nullable=False)
    device_info = db.Column(db.JSON)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    
    login_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_activity = db.Column(db.DateTime, default=datetime.utcnow)
    logout_at = db.Column(db.DateTime)
    expires_at = db.Column(db.DateTime)
    
    is_active = db.Column(db.Boolean, default=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'device_info': self.device_info,
            'ip_address': self.ip_address,
            'login_at': self.login_at.isoformat() if self.login_at else None,
            'last_activity': self.last_activity.isoformat() if self.last_activity else None,
            'is_active': self.is_active
        }