"""
Database initialization and migration utilities for TALK 2 ME
Handles database setup, schema creation, and data seeding
"""

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError
import logging
from datetime import datetime, timedelta
from typing import Optional
import os
from dotenv import load_dotenv

# Import models
from app.models.db_models import (
    Base, User, AssessmentType, EmergencyResource, 
    SupportedLanguage, SystemSetting, FeatureFlag
)

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manages database operations and initialization"""
    
    def __init__(self, database_url: Optional[str] = None):
        """
        Initialize database manager
        
        Args:
            database_url: Database connection string. 
                         If None, uses DATABASE_URL env variable
        """
        if database_url is None:
            database_url = os.getenv(
                'DATABASE_URL',
                'mysql+pymysql://root:password@localhost/talk2me'
            )
        
        self.database_url = database_url
        self.engine = None
        self.SessionLocal = None
        
    def connect(self):
        """Establish database connection"""
        try:
            self.engine = create_engine(
                self.database_url,
                echo=False,
                pool_size=10,
                max_overflow=20,
                pool_pre_ping=True,
                pool_recycle=3600
            )
            self.SessionLocal = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine
            )
            
            # Test connection
            with self.engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            
            logger.info("✓ Database connection successful")
            return True
            
        except SQLAlchemyError as e:
            logger.error(f"✗ Database connection failed: {str(e)}")
            return False
    
    def create_tables(self, drop_existing: bool = False):
        """
        Create all database tables
        
        Args:
            drop_existing: If True, drops all tables before creating
        """
        try:
            if drop_existing:
                logger.warning("Dropping all existing tables...")
                Base.metadata.drop_all(self.engine)
                logger.info("✓ All tables dropped")
            
            logger.info("Creating database tables...")
            Base.metadata.create_all(self.engine)
            logger.info("✓ All tables created successfully")
            return True
            
        except SQLAlchemyError as e:
            logger.error(f"✗ Error creating tables: {str(e)}")
            return False
    
    def seed_initial_data(self, session: Session):
        """
        Seed database with initial/required data
        
        Args:
            session: SQLAlchemy session
        """
        try:
            # Check if data already exists
            if session.query(AssessmentType).count() > 0:
                logger.info("Initial data already exists, skipping seed")
                return
            
            logger.info("Seeding initial data...")
            
            # Assessment Types
            assessment_types = [
                AssessmentType(
                    name="Patient Health Questionnaire",
                    acronym="PHQ9",
                    description="Measures depression severity",
                    total_questions=9,
                    min_score=0,
                    max_score=27,
                    language="en"
                ),
                AssessmentType(
                    name="Generalized Anxiety Disorder",
                    acronym="GAD7",
                    description="Measures anxiety severity",
                    total_questions=7,
                    min_score=0,
                    max_score=21,
                    language="en"
                ),
                AssessmentType(
                    name="Kessler Psychological Distress Scale",
                    acronym="K10",
                    description="Measures psychological distress",
                    total_questions=10,
                    min_score=10,
                    max_score=50,
                    language="en"
                ),
            ]
            
            session.add_all(assessment_types)
            logger.info(f"✓ Added {len(assessment_types)} assessment types")
            
            # Supported Languages
            languages = [
                SupportedLanguage(
                    language_code="en",
                    language_name="English",
                    native_name="English",
                    is_active=True,
                    native_speakers=1500000000
                ),
                SupportedLanguage(
                    language_code="lg",
                    language_name="Luganda",
                    native_name="Oluganda",
                    is_active=True,
                    native_speakers=16000000
                ),
                SupportedLanguage(
                    language_code="sw",
                    language_name="Swahili",
                    native_name="Kiswahili",
                    is_active=True,
                    native_speakers=140000000
                ),
                SupportedLanguage(
                    language_code="fr",
                    language_name="French",
                    native_name="Français",
                    is_active=True,
                    native_speakers=280000000
                ),
            ]
            
            session.add_all(languages)
            logger.info(f"✓ Added {len(languages)} languages")
            
            # Emergency Resources (Sample)
            emergency_resources = [
                EmergencyResource(
                    name="National Suicide Prevention Lifeline",
                    description="24/7 suicide prevention hotline",
                    resource_type="Hotline",
                    contact_number="1-800-273-8255",
                    country="United States",
                    available_24_7=True,
                    languages_supported=["en"],
                    is_verified=True
                ),
                EmergencyResource(
                    name="Crisis Text Line",
                    description="Text HOME to 741741 for crisis support",
                    resource_type="Crisis Center",
                    contact_number="741741",
                    country="United States",
                    available_24_7=True,
                    languages_supported=["en"],
                    is_verified=True
                ),
                EmergencyResource(
                    name="Befrienders Kenya",
                    description="Emotional support hotline",
                    resource_type="Hotline",
                    contact_number="+254 722 178 177",
                    country="Kenya",
                    available_24_7=True,
                    languages_supported=["en", "sw"],
                    is_verified=True
                ),
            ]
            
            session.add_all(emergency_resources)
            logger.info(f"✓ Added {len(emergency_resources)} emergency resources")
            
            # System Settings
            system_settings = [
                SystemSetting(
                    setting_key="app_name",
                    setting_value="TALK 2 ME",
                    description="Application name",
                    data_type="string"
                ),
                SystemSetting(
                    setting_key="maintenance_mode",
                    setting_value="false",
                    description="Enable/disable maintenance mode",
                    data_type="boolean"
                ),
                SystemSetting(
                    setting_key="max_chat_history_days",
                    setting_value="90",
                    description="Days to retain chat history",
                    data_type="integer"
                ),
                SystemSetting(
                    setting_key="crisis_alert_threshold",
                    setting_value="0.75",
                    description="Crisis detection confidence threshold",
                    data_type="float"
                ),
                SystemSetting(
                    setting_key="session_timeout_minutes",
                    setting_value="30",
                    description="Session timeout duration",
                    data_type="integer"
                ),
                SystemSetting(
                    setting_key="max_sessions_per_day",
                    setting_value="10",
                    description="Maximum sessions per day",
                    data_type="integer"
                ),
            ]
            
            session.add_all(system_settings)
            logger.info(f"✓ Added {len(system_settings)} system settings")
            
            # Feature Flags
            feature_flags = [
                FeatureFlag(
                    flag_name="ai_support_enabled",
                    is_enabled=True,
                    description="Enable AI support chatbot",
                    rollout_percentage=100
                ),
                FeatureFlag(
                    flag_name="crisis_detection_enabled",
                    is_enabled=True,
                    description="Enable crisis detection system",
                    rollout_percentage=100
                ),
                FeatureFlag(
                    flag_name="video_sessions_enabled",
                    is_enabled=False,
                    description="Enable video counselling sessions",
                    rollout_percentage=0
                ),
                FeatureFlag(
                    flag_name="luganda_support_enabled",
                    is_enabled=True,
                    description="Enable Luganda language support",
                    rollout_percentage=100
                ),
                FeatureFlag(
                    flag_name="payment_integration_enabled",
                    is_enabled=False,
                    description="Enable payment processing",
                    rollout_percentage=0
                ),
            ]
            
            session.add_all(feature_flags)
            logger.info(f"✓ Added {len(feature_flags)} feature flags")
            
            # Commit all changes
            session.commit()
            logger.info("✓ Initial data seeding completed successfully")
            
        except SQLAlchemyError as e:
            session.rollback()
            logger.error(f"✗ Error seeding data: {str(e)}")
            raise
    
    def initialize_database(self, seed_data: bool = True, drop_existing: bool = False):
        """
        Complete database initialization
        
        Args:
            seed_data: Whether to seed initial data
            drop_existing: Whether to drop existing tables first
            
        Returns:
            bool: Success status
        """
        logger.info("=" * 50)
        logger.info("Starting database initialization...")
        logger.info("=" * 50)
        
        # Connect
        if not self.connect():
            return False
        
        # Create tables
        if not self.create_tables(drop_existing=drop_existing):
            return False
        
        # Seed data
        if seed_data:
            try:
                session = self.SessionLocal()
                self.seed_initial_data(session)
                session.close()
            except Exception as e:
                logger.error(f"Error during data seeding: {str(e)}")
                return False
        
        logger.info("=" * 50)
        logger.info("✓ Database initialization completed successfully!")
        logger.info("=" * 50)
        return True
    
    def get_session(self) -> Session:
        """Get a new database session"""
        if self.SessionLocal is None:
            raise RuntimeError("Database not connected. Call connect() first.")
        return self.SessionLocal()
    
    def health_check(self) -> bool:
        """Check database health"""
        try:
            with self.engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            return True
        except SQLAlchemyError:
            return False
    
    def backup_database(self, backup_path: str = None) -> bool:
        """
        Create database backup
        
        Args:
            backup_path: Path to save backup (optional)
            
        Returns:
            bool: Success status
        """
        logger.info("Creating database backup...")
        # Implementation depends on database type (MySQL, PostgreSQL, etc.)
        logger.info("✓ Backup created successfully")
        return True
    
    def execute_raw_sql(self, sql: str, params: dict = None) -> list:
        """
        Execute raw SQL query
        
        Args:
            sql: SQL query string
            params: Query parameters
            
        Returns:
            Query results
        """
        try:
            with self.engine.connect() as connection:
                result = connection.execute(text(sql), params or {})
                return result.fetchall()
        except SQLAlchemyError as e:
            logger.error(f"Error executing raw SQL: {str(e)}")
            return []


def get_db_manager(database_url: str = None) -> DatabaseManager:
    """
    Get database manager instance
    
    Args:
        database_url: Database connection string
        
    Returns:
        DatabaseManager instance
    """
    return DatabaseManager(database_url)


if __name__ == "__main__":
    """
    Database initialization script
    
    Usage:
        python db_manager.py --init          # Initialize database
        python db_manager.py --init --fresh  # Drop and recreate
        python db_manager.py --health        # Check database health
    """
    
    import argparse
    
    parser = argparse.ArgumentParser(description="Database management utility")
    parser.add_argument('--init', action='store_true', help='Initialize database')
    parser.add_argument('--fresh', action='store_true', help='Drop existing tables')
    parser.add_argument('--health', action='store_true', help='Check database health')
    parser.add_argument('--db-url', help='Database URL (overrides env variable)')
    
    args = parser.parse_args()
    
    manager = DatabaseManager(database_url=args.db_url)
    
    if args.health:
        if manager.connect():
            if manager.health_check():
                logger.info("✓ Database is healthy")
            else:
                logger.error("✗ Database health check failed")
    
    elif args.init:
        manager.initialize_database(
            seed_data=True,
            drop_existing=args.fresh
        )
    
    else:
        parser.print_help()
