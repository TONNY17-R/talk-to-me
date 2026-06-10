-- ============================================================================
-- TALK 2 ME: Comprehensive Mental Health Support System Database Schema
-- ============================================================================
-- This schema includes all tables needed for user management, assessments,
-- chat functionality, counselling, crisis management, and analytics

-- ============================================================================
-- 1. USER MANAGEMENT TABLES
-- ============================================================================

-- Users: Core user information
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    phone_number VARCHAR(20),
    date_of_birth DATE,
    gender ENUM('Male', 'Female', 'Other', 'Prefer not to say'),
    language_preference VARCHAR(50) DEFAULT 'en',
    account_type ENUM('User', 'Counsellor', 'Admin') DEFAULT 'User',
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    last_login DATETIME,
    INDEX idx_email (email),
    INDEX idx_username (username),
    INDEX idx_account_type (account_type)
);

-- User Profiles: Extended user information
CREATE TABLE user_profiles (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL UNIQUE,
    bio TEXT,
    profile_picture_url VARCHAR(500),
    country VARCHAR(100),
    region VARCHAR(100),
    emergency_contact_name VARCHAR(255),
    emergency_contact_phone VARCHAR(20),
    insurance_provider VARCHAR(255),
    insurance_policy_number VARCHAR(255),
    medical_history TEXT,
    medications TEXT,
    allergies TEXT,
    preferred_communication ENUM('Chat', 'Voice', 'Video', 'Email') DEFAULT 'Chat',
    notifications_enabled BOOLEAN DEFAULT TRUE,
    marketing_emails_enabled BOOLEAN DEFAULT FALSE,
    privacy_level ENUM('Public', 'Private', 'Friends Only') DEFAULT 'Private',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id)
);

-- Counsellors: Information about professional counsellors
CREATE TABLE counsellors (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL UNIQUE,
    license_number VARCHAR(255) UNIQUE NOT NULL,
    specializations TEXT, -- JSON array or comma-separated
    qualifications TEXT,
    experience_years INT,
    bio TEXT,
    hourly_rate DECIMAL(10, 2),
    availability_status ENUM('Available', 'Busy', 'Offline') DEFAULT 'Offline',
    is_verified BOOLEAN DEFAULT FALSE,
    verification_date DATETIME,
    rating DECIMAL(3, 2) DEFAULT 0,
    total_sessions INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_availability_status (availability_status)
);

-- ============================================================================
-- 2. AUTHENTICATION & SECURITY TABLES
-- ============================================================================

-- Password Reset Tokens
CREATE TABLE password_reset_tokens (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    token VARCHAR(500) UNIQUE NOT NULL,
    expires_at DATETIME NOT NULL,
    used BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_token (token)
);

-- Email Verification Tokens
CREATE TABLE email_verification_tokens (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    token VARCHAR(500) UNIQUE NOT NULL,
    expires_at DATETIME NOT NULL,
    verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id)
);

-- Login History
CREATE TABLE login_history (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    ip_address VARCHAR(45),
    user_agent TEXT,
    login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    logout_time DATETIME,
    device_type VARCHAR(50),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_login_time (login_time)
);

-- ============================================================================
-- 3. ASSESSMENT TABLES
-- ============================================================================

-- Assessment Types
CREATE TABLE assessment_types (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    acronym VARCHAR(50) UNIQUE,
    description TEXT,
    total_questions INT,
    min_score INT,
    max_score INT,
    language VARCHAR(50) DEFAULT 'en',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_acronym (acronym)
);

-- Assessments: User assessment responses
CREATE TABLE assessments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    assessment_type_id INT NOT NULL,
    responses JSON, -- Stores question-answer pairs
    total_score INT,
    risk_level ENUM('Low', 'Moderate', 'High', 'Severe') DEFAULT 'Low',
    interpretation TEXT,
    recommendations TEXT,
    completed_at DATETIME NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (assessment_type_id) REFERENCES assessment_types(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_assessment_type_id (assessment_type_id),
    INDEX idx_completed_at (completed_at),
    INDEX idx_risk_level (risk_level)
);

-- Assessment Progress Tracker
CREATE TABLE assessment_progress (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    assessment_type_id INT NOT NULL,
    previous_score INT,
    current_score INT,
    score_change INT,
    improvement_percentage DECIMAL(5, 2),
    days_since_last_assessment INT,
    trend VARCHAR(50), -- 'Improving', 'Declining', 'Stable'
    tracked_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (assessment_type_id) REFERENCES assessment_types(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id)
);

-- ============================================================================
-- 4. CHAT & MESSAGING TABLES
-- ============================================================================

-- Chat Conversations
CREATE TABLE chat_conversations (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    counsellor_id INT,
    conversation_type ENUM('User-AI', 'User-Counsellor', 'Group') DEFAULT 'User-AI',
    title VARCHAR(255),
    status ENUM('Active', 'Closed', 'Archived') DEFAULT 'Active',
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ended_at DATETIME,
    total_messages INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (counsellor_id) REFERENCES counsellors(id) ON DELETE SET NULL,
    INDEX idx_user_id (user_id),
    INDEX idx_status (status),
    INDEX idx_started_at (started_at)
);

-- Chat Messages
CREATE TABLE chat_messages (
    id INT PRIMARY KEY AUTO_INCREMENT,
    conversation_id INT NOT NULL,
    sender_id INT NOT NULL,
    sender_type ENUM('User', 'Counsellor', 'AI') DEFAULT 'User',
    message_text TEXT NOT NULL,
    message_type ENUM('Text', 'Image', 'Audio', 'File', 'Emoji') DEFAULT 'Text',
    file_url VARCHAR(500),
    is_read BOOLEAN DEFAULT FALSE,
    read_at DATETIME,
    sentiment_score DECIMAL(3, 2), -- AI-detected sentiment
    sentiment_label ENUM('Positive', 'Neutral', 'Negative'),
    crisis_detected BOOLEAN DEFAULT FALSE,
    crisis_keywords TEXT, -- JSON array of detected keywords
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (conversation_id) REFERENCES chat_conversations(id) ON DELETE CASCADE,
    FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_conversation_id (conversation_id),
    INDEX idx_sender_id (sender_id),
    INDEX idx_created_at (created_at),
    INDEX idx_crisis_detected (crisis_detected)
);

-- Message Reactions (Emoji reactions)
CREATE TABLE message_reactions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    message_id INT NOT NULL,
    user_id INT NOT NULL,
    reaction_emoji VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (message_id) REFERENCES chat_messages(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_reaction (message_id, user_id),
    INDEX idx_message_id (message_id)
);

-- ============================================================================
-- 5. CRISIS MANAGEMENT TABLES
-- ============================================================================

-- Crisis Alerts
CREATE TABLE crisis_alerts (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    message_id INT,
    alert_type ENUM('Keyword Detection', 'Manual Report', 'Pattern Detection') DEFAULT 'Keyword Detection',
    severity ENUM('Low', 'Medium', 'High', 'Critical') DEFAULT 'High',
    keywords_detected TEXT, -- JSON array
    description TEXT,
    status ENUM('Active', 'In Review', 'Resolved', 'False Alarm') DEFAULT 'Active',
    assigned_to INT, -- counsellor_id
    reviewed_by INT, -- admin_id
    action_taken TEXT,
    review_notes TEXT,
    resolved_at DATETIME,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (message_id) REFERENCES chat_messages(id) ON DELETE SET NULL,
    FOREIGN KEY (assigned_to) REFERENCES counsellors(id) ON DELETE SET NULL,
    INDEX idx_user_id (user_id),
    INDEX idx_severity (severity),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at)
);

-- Emergency Resources
CREATE TABLE emergency_resources (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    resource_type ENUM('Hotline', 'Hospital', 'Crisis Center', 'Website', 'App') DEFAULT 'Hotline',
    contact_number VARCHAR(20),
    email VARCHAR(255),
    website_url VARCHAR(500),
    address TEXT,
    country VARCHAR(100),
    region VARCHAR(100),
    available_24_7 BOOLEAN DEFAULT TRUE,
    languages_supported TEXT, -- JSON array
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_country (country),
    INDEX idx_resource_type (resource_type)
);

-- ============================================================================
-- 6. COUNSELLING TABLES
-- ============================================================================

-- Counselling Sessions
CREATE TABLE counselling_sessions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    counsellor_id INT NOT NULL,
    session_type ENUM('Individual', 'Group', 'Crisis') DEFAULT 'Individual',
    communication_method ENUM('Chat', 'Voice', 'Video') DEFAULT 'Chat',
    scheduled_at DATETIME,
    started_at DATETIME,
    ended_at DATETIME,
    duration_minutes INT,
    status ENUM('Scheduled', 'In Progress', 'Completed', 'Cancelled', 'No-show') DEFAULT 'Scheduled',
    notes TEXT,
    session_plan TEXT,
    outcome TEXT,
    follow_up_required BOOLEAN DEFAULT FALSE,
    follow_up_date DATETIME,
    cost DECIMAL(10, 2),
    payment_status ENUM('Pending', 'Paid', 'Refunded') DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (counsellor_id) REFERENCES counsellors(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_counsellor_id (counsellor_id),
    INDEX idx_status (status),
    INDEX idx_scheduled_at (scheduled_at)
);

-- Counselling Session Notes
CREATE TABLE session_notes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    session_id INT NOT NULL UNIQUE,
    clinical_notes TEXT,
    diagnosis_notes TEXT,
    treatment_plan TEXT,
    medications_prescribed TEXT,
    referrals TEXT,
    follow_up_instructions TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES counselling_sessions(id) ON DELETE CASCADE
);

-- ============================================================================
-- 7. RESOURCES & CONTENT TABLES
-- ============================================================================

-- Resources (Articles, Videos, etc.)
CREATE TABLE resources (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    content_type ENUM('Article', 'Video', 'Audio', 'Document', 'Interactive') DEFAULT 'Article',
    content_url VARCHAR(500),
    category VARCHAR(100),
    subcategory VARCHAR(100),
    tags TEXT, -- JSON array
    language VARCHAR(50) DEFAULT 'en',
    author VARCHAR(255),
    source VARCHAR(255),
    is_published BOOLEAN DEFAULT FALSE,
    view_count INT DEFAULT 0,
    rating DECIMAL(3, 2) DEFAULT 0,
    difficulty_level ENUM('Beginner', 'Intermediate', 'Advanced') DEFAULT 'Beginner',
    estimated_read_time_minutes INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_category (category),
    INDEX idx_language (language),
    INDEX idx_is_published (is_published)
);

-- Resource Views Tracking
CREATE TABLE resource_views (
    id INT PRIMARY KEY AUTO_INCREMENT,
    resource_id INT NOT NULL,
    user_id INT,
    viewed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    time_spent_seconds INT,
    completed BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (resource_id) REFERENCES resources(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_resource_id (resource_id),
    INDEX idx_user_id (user_id)
);

-- Resource Ratings
CREATE TABLE resource_ratings (
    id INT PRIMARY KEY AUTO_INCREMENT,
    resource_id INT NOT NULL,
    user_id INT NOT NULL,
    rating INT CHECK (rating >= 1 AND rating <= 5),
    review_text TEXT,
    helpful_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (resource_id) REFERENCES resources(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_rating (resource_id, user_id),
    INDEX idx_resource_id (resource_id)
);

-- ============================================================================
-- 8. PAYMENT & SUBSCRIPTION TABLES
-- ============================================================================

-- Payment Transactions
CREATE TABLE payments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    transaction_type ENUM('Session', 'Subscription', 'Resource Purchase', 'Donation') DEFAULT 'Session',
    amount DECIMAL(10, 2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'USD',
    payment_method ENUM('Credit Card', 'Debit Card', 'Mobile Money', 'Bank Transfer', 'PayPal') DEFAULT 'Credit Card',
    payment_gateway VARCHAR(100),
    transaction_id VARCHAR(255) UNIQUE,
    reference_id INT, -- Could be session_id, subscription_id, etc.
    status ENUM('Pending', 'Completed', 'Failed', 'Refunded', 'Cancelled') DEFAULT 'Pending',
    error_message TEXT,
    receipt_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at)
);

-- Subscriptions
CREATE TABLE subscriptions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    plan_type ENUM('Free', 'Basic', 'Professional', 'Premium') DEFAULT 'Free',
    subscription_status ENUM('Active', 'Paused', 'Cancelled', 'Expired') DEFAULT 'Active',
    start_date DATE,
    end_date DATE,
    auto_renew BOOLEAN DEFAULT TRUE,
    sessions_limit INT,
    sessions_used INT DEFAULT 0,
    storage_limit_gb INT,
    storage_used_gb DECIMAL(10, 2) DEFAULT 0,
    features TEXT, -- JSON array of enabled features
    price DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_subscription_status (subscription_status)
);

-- ============================================================================
-- 9. NOTIFICATION TABLES
-- ============================================================================

-- Notifications
CREATE TABLE notifications (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    notification_type ENUM('Message', 'Session', 'Alert', 'Resource', 'System') DEFAULT 'System',
    title VARCHAR(255),
    message TEXT NOT NULL,
    related_id INT, -- Could be message_id, session_id, etc.
    is_read BOOLEAN DEFAULT FALSE,
    read_at DATETIME,
    action_url VARCHAR(500),
    priority ENUM('Low', 'Medium', 'High', 'Critical') DEFAULT 'Medium',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_is_read (is_read),
    INDEX idx_created_at (created_at)
);

-- SMS Notifications Log
CREATE TABLE sms_log (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    phone_number VARCHAR(20),
    message TEXT,
    status ENUM('Pending', 'Sent', 'Failed', 'Delivered') DEFAULT 'Pending',
    message_id VARCHAR(255),
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sent_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id)
);

-- Email Notifications Log
CREATE TABLE email_log (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    email_address VARCHAR(255),
    subject VARCHAR(255),
    message_type VARCHAR(100),
    status ENUM('Pending', 'Sent', 'Failed', 'Bounced') DEFAULT 'Pending',
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sent_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_status (status)
);

-- ============================================================================
-- 10. ANALYTICS & REPORTING TABLES
-- ============================================================================

-- User Analytics
CREATE TABLE user_analytics (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    total_sessions INT DEFAULT 0,
    total_messages INT DEFAULT 0,
    assessments_completed INT DEFAULT 0,
    resources_viewed INT DEFAULT 0,
    average_sentiment_score DECIMAL(3, 2),
    crisis_incidents INT DEFAULT 0,
    last_active_date DATETIME,
    engagement_score DECIMAL(5, 2) DEFAULT 0,
    tracked_date DATE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_date (user_id, tracked_date),
    INDEX idx_user_id (user_id)
);

-- System Analytics
CREATE TABLE system_analytics (
    id INT PRIMARY KEY AUTO_INCREMENT,
    tracked_date DATE NOT NULL UNIQUE,
    total_active_users INT,
    new_users_today INT,
    total_sessions_today INT,
    total_messages_today INT,
    crisis_alerts_today INT,
    average_session_duration_minutes DECIMAL(10, 2),
    server_uptime_percentage DECIMAL(5, 2),
    error_count INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- AI Model Performance Tracking
CREATE TABLE ai_model_performance (
    id INT PRIMARY KEY AUTO_INCREMENT,
    model_name VARCHAR(255),
    model_version VARCHAR(50),
    metric_type ENUM('Accuracy', 'Precision', 'Recall', 'F1-Score') DEFAULT 'Accuracy',
    metric_value DECIMAL(5, 4),
    test_dataset_size INT,
    tested_at DATETIME,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_model_name (model_name)
);

-- ============================================================================
-- 11. ADMIN & MODERATION TABLES
-- ============================================================================

-- Admin Actions Log
CREATE TABLE admin_actions_log (
    id INT PRIMARY KEY AUTO_INCREMENT,
    admin_id INT NOT NULL,
    action_type VARCHAR(100),
    entity_type VARCHAR(100), -- 'User', 'Message', 'Session', etc.
    entity_id INT,
    old_value TEXT,
    new_value TEXT,
    reason TEXT,
    ip_address VARCHAR(45),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (admin_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_admin_id (admin_id),
    INDEX idx_action_type (action_type),
    INDEX idx_created_at (created_at)
);

-- Content Moderation
CREATE TABLE content_moderation (
    id INT PRIMARY KEY AUTO_INCREMENT,
    content_type ENUM('Message', 'Comment', 'Review', 'Resource') DEFAULT 'Message',
    content_id INT,
    reported_by INT,
    reason ENUM('Spam', 'Offensive', 'Misinformation', 'Harmful', 'Other') DEFAULT 'Other',
    description TEXT,
    status ENUM('Reported', 'Under Review', 'Approved', 'Rejected', 'Deleted') DEFAULT 'Reported',
    reviewed_by INT, -- admin_id
    moderation_note TEXT,
    action_taken TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    reviewed_at DATETIME,
    FOREIGN KEY (reported_by) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (reviewed_by) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_status (status),
    INDEX idx_created_at (created_at)
);

-- User Reports
CREATE TABLE user_reports (
    id INT PRIMARY KEY AUTO_INCREMENT,
    reported_user_id INT NOT NULL,
    reported_by INT NOT NULL,
    report_type ENUM('Harassment', 'Abuse', 'Spam', 'Impersonation', 'Other') DEFAULT 'Other',
    description TEXT,
    status ENUM('Reported', 'Under Review', 'Resolved', 'Dismissed') DEFAULT 'Reported',
    action_taken VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (reported_user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (reported_by) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_reported_user_id (reported_user_id),
    INDEX idx_status (status)
);

-- ============================================================================
-- 12. SYSTEM CONFIGURATION TABLES
-- ============================================================================

-- System Settings
CREATE TABLE system_settings (
    id INT PRIMARY KEY AUTO_INCREMENT,
    setting_key VARCHAR(255) UNIQUE NOT NULL,
    setting_value TEXT,
    description TEXT,
    data_type VARCHAR(50), -- 'string', 'integer', 'boolean', 'json'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_setting_key (setting_key)
);

-- Feature Flags
CREATE TABLE feature_flags (
    id INT PRIMARY KEY AUTO_INCREMENT,
    flag_name VARCHAR(255) UNIQUE NOT NULL,
    is_enabled BOOLEAN DEFAULT FALSE,
    description TEXT,
    rollout_percentage INT DEFAULT 100,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_flag_name (flag_name)
);

-- ============================================================================
-- 13. DATA BACKUP & AUDIT TABLES
-- ============================================================================

-- Audit Trail
CREATE TABLE audit_trail (
    id INT PRIMARY KEY AUTO_INCREMENT,
    table_name VARCHAR(100),
    record_id INT,
    operation ENUM('INSERT', 'UPDATE', 'DELETE') NOT NULL,
    old_data JSON,
    new_data JSON,
    changed_by INT,
    change_reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (changed_by) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_table_name (table_name),
    INDEX idx_created_at (created_at)
);

-- Data Retention Policy
CREATE TABLE data_retention_policies (
    id INT PRIMARY KEY AUTO_INCREMENT,
    table_name VARCHAR(100),
    retention_days INT,
    auto_delete BOOLEAN DEFAULT FALSE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- ============================================================================
-- 14. SUPPORT & FEEDBACK TABLES
-- ============================================================================

-- User Feedback
CREATE TABLE user_feedback (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    feedback_type ENUM('Bug Report', 'Feature Request', 'Improvement', 'General Feedback') DEFAULT 'General Feedback',
    category VARCHAR(100),
    subject VARCHAR(255),
    message TEXT NOT NULL,
    attachment_url VARCHAR(500),
    status ENUM('New', 'In Review', 'Acknowledged', 'Resolved') DEFAULT 'New',
    response TEXT,
    responded_by INT,
    rating INT CHECK (rating >= 1 AND rating <= 5),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (responded_by) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_status (status),
    INDEX idx_created_at (created_at)
);

-- Support Tickets
CREATE TABLE support_tickets (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    ticket_number VARCHAR(50) UNIQUE NOT NULL,
    subject VARCHAR(255) NOT NULL,
    description TEXT,
    category VARCHAR(100),
    priority ENUM('Low', 'Medium', 'High', 'Critical') DEFAULT 'Medium',
    status ENUM('Open', 'In Progress', 'Waiting for User', 'Resolved', 'Closed') DEFAULT 'Open',
    assigned_to INT, -- admin or support staff
    resolution TEXT,
    resolved_at DATETIME,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (assigned_to) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_user_id (user_id),
    INDEX idx_status (status),
    INDEX idx_priority (priority)
);

-- Support Ticket Responses
CREATE TABLE support_ticket_responses (
    id INT PRIMARY KEY AUTO_INCREMENT,
    ticket_id INT NOT NULL,
    responder_id INT NOT NULL,
    response_text TEXT NOT NULL,
    attachment_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ticket_id) REFERENCES support_tickets(id) ON DELETE CASCADE,
    FOREIGN KEY (responder_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_ticket_id (ticket_id)
);

-- ============================================================================
-- 15. TRANSLATION & LOCALIZATION TABLES
-- ============================================================================

-- Supported Languages
CREATE TABLE supported_languages (
    id INT PRIMARY KEY AUTO_INCREMENT,
    language_code VARCHAR(10) UNIQUE NOT NULL,
    language_name VARCHAR(100) NOT NULL,
    native_name VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    native_speakers INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Translations
CREATE TABLE translations (
    id INT PRIMARY KEY AUTO_INCREMENT,
    language_code VARCHAR(10) NOT NULL,
    translation_key VARCHAR(255) NOT NULL,
    translation_value TEXT NOT NULL,
    context VARCHAR(100),
    translator_id INT,
    is_reviewed BOOLEAN DEFAULT FALSE,
    reviewed_by INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY unique_translation (language_code, translation_key),
    FOREIGN KEY (language_code) REFERENCES supported_languages(language_code) ON DELETE CASCADE,
    INDEX idx_language_code (language_code)
);

-- ============================================================================
-- INDEXES FOR OPTIMIZATION
-- ============================================================================

-- Additional performance indexes
CREATE INDEX idx_assessments_user_type ON assessments(user_id, assessment_type_id);
CREATE INDEX idx_messages_conversation_time ON chat_messages(conversation_id, created_at);
CREATE INDEX idx_sessions_user_counsellor ON counselling_sessions(user_id, counsellor_id);
CREATE INDEX idx_crisis_user_status ON crisis_alerts(user_id, status);
CREATE INDEX idx_payments_user_status ON payments(user_id, status);
CREATE INDEX idx_notifications_user_read ON notifications(user_id, is_read);

-- ============================================================================
-- END OF DATABASE SCHEMA
-- ============================================================================
