-- ============================================================================
-- TALK 2 ME: Advanced Features Database Schema Extensions
-- ============================================================================
-- This file extends the existing schema with tables for:
-- 1. Predictive Analytics & Intervention
-- 2. Voice & Audio Biomarkers
-- 3. Peer Support Network
-- 4. Gamification & Behavioral Science
-- 5. Real-Time Crisis Command Center
-- 6. Digital Therapeutics
-- 7. Advanced Analytics
-- 8. Integration Ecosystem
-- 9. Security & Compliance

-- ============================================================================
-- 1. PREDICTIVE ANALYTICS & INTERVENTION TABLES
-- ============================================================================

-- Mental Health Trajectory Predictions
CREATE TABLE mental_health_predictions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    prediction_type ENUM('decline', 'improvement', 'relapse_risk', 'suicide_risk') NOT NULL,
    confidence_score FLOAT NOT NULL COMMENT 'ML confidence 0-1',
    predicted_severity ENUM('low', 'medium', 'high', 'critical') NOT NULL,
    predicted_date DATE NOT NULL,
    factors JSON NOT NULL COMMENT 'Contributing factors',
    recommended_intervention TEXT,
    intervention_timing ENUM('immediate', 'within_24h', 'within_week', 'scheduled') DEFAULT 'scheduled',
    status ENUM('pending', 'actioned', 'cancelled', 'completed') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_prediction (user_id, prediction_type),
    INDEX idx_predicted_date (predicted_date),
    INDEX idx_status (status)
);

-- Risk Stratification Tiers
CREATE TABLE user_risk_tiers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL UNIQUE,
    current_tier ENUM('low', 'medium', 'high', 'critical') NOT NULL,
    phq9_score INT,
    gad7_score INT,
    crisis_keywords_detected INT DEFAULT 0,
    failed_sessions INT DEFAULT 0,
    days_without_engagement INT DEFAULT 0,
    self_harm_indicators INT DEFAULT 0,
    substance_use_indicators INT DEFAULT 0,
    isolation_score FLOAT DEFAULT 0,
    tier_updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    next_reassessment_date DATE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_tier (current_tier),
    INDEX idx_next_reassessment (next_reassessment_date)
);

-- Intervention History & Outcomes
CREATE TABLE interventions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    prediction_id INT,
    intervention_type VARCHAR(100) NOT NULL COMMENT 'email_outreach, sms_check_in, app_notification, counselor_assignment',
    description TEXT,
    delivery_channel ENUM('sms', 'email', 'push', 'whatsapp', 'counselor', 'emergency') NOT NULL,
    status ENUM('pending', 'sent', 'delivered', 'opened', 'engaged', 'failed') DEFAULT 'pending',
    outcome_score INT COMMENT 'Post-intervention assessment score change',
    user_response TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (prediction_id) REFERENCES mental_health_predictions(id) ON DELETE SET NULL,
    INDEX idx_user_intervention (user_id, created_at),
    INDEX idx_status (status)
);

-- ============================================================================
-- 2. VOICE & AUDIO BIOMARKERS TABLES
-- ============================================================================

-- Voice Recordings & Analysis
CREATE TABLE voice_recordings (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    chat_id INT,
    counselor_id INT,
    recording_url VARCHAR(500) NOT NULL,
    duration_seconds INT NOT NULL,
    language ENUM('en', 'lg', 'sw') DEFAULT 'en',
    transcription LONGTEXT,
    is_transcribed BOOLEAN DEFAULT FALSE,
    recording_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_recordings (user_id, recording_date)
);

-- Voice Emotion & Biomarker Analysis
CREATE TABLE voice_biomarkers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    recording_id INT NOT NULL UNIQUE,
    emotion_detected ENUM('neutral', 'happy', 'sad', 'anxious', 'angry', 'depressed') NOT NULL,
    emotion_confidence FLOAT,
    speech_rate FLOAT COMMENT 'words per minute',
    pitch_average FLOAT COMMENT 'Hz',
    pitch_variance FLOAT,
    voice_intensity FLOAT,
    pause_frequency INT,
    stutter_frequency INT,
    vocal_fry_detected BOOLEAN DEFAULT FALSE,
    depression_indicators INT DEFAULT 0,
    anxiety_indicators INT DEFAULT 0,
    suicidality_risk_score FLOAT DEFAULT 0,
    overall_mental_state VARCHAR(100),
    analysis_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (recording_id) REFERENCES voice_recordings(id) ON DELETE CASCADE,
    INDEX idx_analysis_date (analysis_timestamp)
);

-- Speech Pattern Trends
CREATE TABLE speech_patterns (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    week_starting DATE NOT NULL,
    avg_speech_rate FLOAT,
    avg_pitch FLOAT,
    avg_intensity FLOAT,
    total_pause_time INT COMMENT 'seconds',
    average_utterance_length INT COMMENT 'words',
    lexical_diversity FLOAT,
    trend_direction ENUM('improving', 'stable', 'declining') DEFAULT 'stable',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_week (user_id, week_starting),
    INDEX idx_user_trends (user_id, week_starting)
);

-- ============================================================================
-- 3. PEER SUPPORT NETWORK TABLES
-- ============================================================================

-- Peer Support Groups
CREATE TABLE peer_support_groups (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    topic ENUM('depression', 'anxiety', 'trauma', 'substance_abuse', 'recovery', 'general', 'women_specific', 'men_specific', 'lgbtq', 'youth') NOT NULL,
    max_members INT DEFAULT 15,
    moderator_id INT NOT NULL,
    language ENUM('en', 'lg', 'sw') DEFAULT 'en',
    is_active BOOLEAN DEFAULT TRUE,
    moderation_mode ENUM('automated', 'manual', 'hybrid') DEFAULT 'hybrid',
    meeting_schedule JSON COMMENT '{"day": "Monday", "time": "14:00"}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (moderator_id) REFERENCES users(id) ON DELETE RESTRICT,
    INDEX idx_topic (topic),
    INDEX idx_active (is_active)
);

-- Peer Group Memberships
CREATE TABLE peer_group_members (
    id INT PRIMARY KEY AUTO_INCREMENT,
    group_id INT NOT NULL,
    user_id INT NOT NULL,
    role ENUM('member', 'mentor', 'moderator') DEFAULT 'member',
    joined_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('active', 'inactive', 'suspended') DEFAULT 'active',
    FOREIGN KEY (group_id) REFERENCES peer_support_groups(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_group_member (group_id, user_id),
    INDEX idx_user_groups (user_id)
);

-- Peer Matching Profiles
CREATE TABLE peer_matching_profiles (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL UNIQUE,
    primary_condition ENUM('depression', 'anxiety', 'trauma', 'substance_abuse', 'bipolar', 'schizophrenia', 'eating_disorder', 'other') NOT NULL,
    recovery_stage ENUM('crisis', 'early_recovery', 'ongoing_recovery', 'maintenance', 'recovered') NOT NULL,
    preferred_peer_type ENUM('similar_condition', 'further_ahead', 'professional_peer', 'diverse') NOT NULL,
    matching_score FLOAT DEFAULT 0,
    last_matched_user_id INT,
    match_success_rating FLOAT COMMENT '1-5 scale',
    can_be_mentor BOOLEAN DEFAULT FALSE,
    mentor_experience_years FLOAT,
    mentor_credentials JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_condition_stage (primary_condition, recovery_stage)
);

-- Peer Interactions & Outcomes
CREATE TABLE peer_interactions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    mentor_id INT NOT NULL,
    mentee_id INT NOT NULL,
    interaction_type ENUM('chat', 'video_call', 'group_session', 'resource_share') NOT NULL,
    duration_minutes INT,
    sentiment_analysis JSON COMMENT '{"mentee_sentiment": "positive", "mentor_sentiment": "positive"}',
    mentee_rating FLOAT COMMENT '1-5 scale',
    mentor_notes TEXT,
    outcome_indicator ENUM('positive', 'neutral', 'negative', 'not_applicable') DEFAULT 'not_applicable',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (mentor_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (mentee_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_mentor_mentee (mentor_id, mentee_id, created_at)
);

-- ============================================================================
-- 4. GAMIFICATION & BEHAVIORAL SCIENCE TABLES
-- ============================================================================

-- User Habits & Streaks
CREATE TABLE user_habits (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    habit_type ENUM('mood_check_in', 'meditation', 'exercise', 'sleep_tracking', 'journaling', 'therapy_session', 'medication_adherence', 'social_connection', 'resource_learning') NOT NULL,
    frequency_goal ENUM('daily', 'weekly', 'custom') DEFAULT 'daily',
    current_streak INT DEFAULT 0,
    longest_streak INT DEFAULT 0,
    completion_count INT DEFAULT 0,
    last_completed_date DATE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_habits (user_id, is_active)
);

-- Daily Habit Logs
CREATE TABLE habit_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    habit_id INT NOT NULL,
    user_id INT NOT NULL,
    log_date DATE NOT NULL,
    completion_status ENUM('completed', 'skipped', 'partial') DEFAULT 'completed',
    notes TEXT,
    score INT COMMENT 'Difficulty rating or effort score',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (habit_id) REFERENCES user_habits(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_habit_date (habit_id, log_date),
    INDEX idx_user_date (user_id, log_date)
);

-- Gamification Achievements & Badges
CREATE TABLE achievements (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL UNIQUE,
    description TEXT,
    badge_image_url VARCHAR(500),
    category ENUM('milestone', 'consistency', 'engagement', 'progress', 'peer_support', 'recovery') NOT NULL,
    criteria JSON NOT NULL COMMENT '{"type": "streak", "value": 30, "unit": "days"}',
    reward_points INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User Achievements
CREATE TABLE user_achievements (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    achievement_id INT NOT NULL,
    unlocked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (achievement_id) REFERENCES achievements(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_achievement (user_id, achievement_id),
    INDEX idx_user_achievements (user_id)
);

-- User Gamification Profile
CREATE TABLE gamification_profiles (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL UNIQUE,
    total_points INT DEFAULT 0,
    level INT DEFAULT 1,
    points_to_next_level INT DEFAULT 1000,
    current_streak_days INT DEFAULT 0,
    total_achievements_unlocked INT DEFAULT 0,
    leaderboard_position INT,
    opted_in_leaderboard BOOLEAN DEFAULT FALSE,
    readiness_stage ENUM('precontemplation', 'contemplation', 'preparation', 'action', 'maintenance') DEFAULT 'precontemplation',
    last_engagement TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_leaderboard (opted_in_leaderboard, total_points DESC)
);

-- ============================================================================
-- 5. CRISIS COMMAND CENTER TABLES
-- ============================================================================

-- Enhanced Crisis Alerts
CREATE TABLE crisis_alerts_advanced (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    alert_level ENUM('warning', 'severe', 'critical', 'emergency') NOT NULL,
    detection_method ENUM('text_analysis', 'voice_analysis', 'pattern_change', 'user_self_report', 'behavioral_trigger') NOT NULL,
    trigger_data JSON NOT NULL COMMENT 'What triggered the alert',
    confidence_score FLOAT,
    multimodal_score FLOAT COMMENT 'Combined score from multiple sources',
    assigned_counselor_id INT,
    assigned_responder_id INT,
    emergency_contact_notified BOOLEAN DEFAULT FALSE,
    emergency_contact_response TEXT,
    location_data JSON COMMENT '{"lat": 0.0, "lon": 32.0, "accuracy": 50}',
    response_status ENUM('pending', 'acknowledged', 'in_progress', 'resolved', 'escalated') DEFAULT 'pending',
    resolution_notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (assigned_counselor_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_alert_level (alert_level),
    INDEX idx_response_status (response_status),
    INDEX idx_created_at (created_at DESC)
);

-- Crisis Session Transcripts & AI Analysis
CREATE TABLE crisis_sessions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    counselor_id INT NOT NULL,
    session_start TIMESTAMP,
    session_end TIMESTAMP,
    transcript LONGTEXT,
    ai_analysis JSON COMMENT '{"suicidality": 0.8, "self_harm": 0.3, "homicidality": 0.1, "psychosis": 0.2}',
    ai_recommended_actions TEXT,
    session_outcome ENUM('stabilized', 'referred_to_hospital', 'referred_to_specialist', 'follow_up_scheduled', 'ongoing') DEFAULT 'follow_up_scheduled',
    follow_up_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (counselor_id) REFERENCES users(id) ON DELETE RESTRICT,
    INDEX idx_user_sessions (user_id, session_start)
);

-- Crisis Event Timeline
CREATE TABLE crisis_timeline (
    id INT PRIMARY KEY AUTO_INCREMENT,
    alert_id INT NOT NULL,
    event_type ENUM('alert_triggered', 'counselor_assigned', 'emergency_contact_notified', 'video_session_started', 'user_hospitalized', 'crisis_resolved', 'follow_up_scheduled') NOT NULL,
    actor_id INT COMMENT 'Who performed the action',
    event_details TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (alert_id) REFERENCES crisis_alerts_advanced(id) ON DELETE CASCADE,
    INDEX idx_alert_timeline (alert_id, timestamp)
);

-- ============================================================================
-- 6. DIGITAL THERAPEUTICS TABLES
-- ============================================================================

-- Digital Therapy Programs
CREATE TABLE therapy_programs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    program_type ENUM('cbt', 'dbt', 'exposure_therapy', 'mindfulness', 'sleep_training', 'substance_abuse', 'trauma_focused') NOT NULL,
    description TEXT,
    duration_weeks INT,
    weekly_sessions INT DEFAULT 2,
    difficulty_level ENUM('beginner', 'intermediate', 'advanced') DEFAULT 'beginner',
    evidence_base VARCHAR(255) COMMENT 'Research citations',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Therapy Program Modules
CREATE TABLE therapy_modules (
    id INT PRIMARY KEY AUTO_INCREMENT,
    program_id INT NOT NULL,
    module_number INT NOT NULL,
    module_title VARCHAR(255) NOT NULL,
    description TEXT,
    learning_objectives JSON,
    duration_minutes INT,
    content_url VARCHAR(500),
    interactive_exercises JSON COMMENT 'List of exercise IDs',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (program_id) REFERENCES therapy_programs(id) ON DELETE CASCADE,
    INDEX idx_program_modules (program_id, module_number)
);

-- User Therapy Enrollment
CREATE TABLE user_therapy_enrollment (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    program_id INT NOT NULL,
    enrollment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('active', 'paused', 'completed', 'dropped_out') DEFAULT 'active',
    current_module INT DEFAULT 1,
    completion_percentage FLOAT DEFAULT 0,
    last_activity_date TIMESTAMP,
    therapist_notes TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (program_id) REFERENCES therapy_programs(id) ON DELETE RESTRICT,
    INDEX idx_user_program (user_id, program_id)
);

-- Interactive Therapy Exercises
CREATE TABLE therapy_exercises (
    id INT PRIMARY KEY AUTO_INCREMENT,
    module_id INT NOT NULL,
    exercise_name VARCHAR(255) NOT NULL,
    exercise_type ENUM('cbt_worksheet', 'exposure_scenario', 'breathing_exercise', 'meditation_guided', 'journal_prompt', 'behavioral_activation', 'thought_record') NOT NULL,
    instructions TEXT,
    duration_minutes INT,
    difficulty_rating INT COMMENT '1-10 scale',
    evidence_effectiveness FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (module_id) REFERENCES therapy_modules(id) ON DELETE CASCADE,
    INDEX idx_module_exercises (module_id)
);

-- Exercise Completions & Progress
CREATE TABLE exercise_completions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    exercise_id INT NOT NULL,
    completion_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    duration_spent_minutes INT,
    user_rating INT COMMENT '1-5 difficulty rating',
    exercise_notes TEXT,
    ai_feedback TEXT COMMENT 'Auto-generated feedback from AI analysis',
    symptom_change_reported INT COMMENT '-10 to 10 scale',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (exercise_id) REFERENCES therapy_exercises(id) ON DELETE CASCADE,
    INDEX idx_user_exercises (user_id, completion_date)
);

-- ============================================================================
-- 7. ADVANCED ANALYTICS TABLES
-- ============================================================================

-- Population Mental Health Metrics
CREATE TABLE population_mental_health_dashboard (
    id INT PRIMARY KEY AUTO_INCREMENT,
    reporting_date DATE NOT NULL UNIQUE,
    region VARCHAR(100),
    age_group VARCHAR(50),
    gender VARCHAR(50),
    total_users INT DEFAULT 0,
    avg_phq9_score FLOAT,
    avg_gad7_score FLOAT,
    depression_prevalence_percentage FLOAT,
    anxiety_prevalence_percentage FLOAT,
    crisis_alerts_count INT DEFAULT 0,
    crisis_hospitalization_count INT DEFAULT 0,
    completed_therapy_sessions INT DEFAULT 0,
    substance_use_incidence INT DEFAULT 0,
    suicide_attempts INT DEFAULT 0,
    successful_interventions INT DEFAULT 0,
    user_retention_rate FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Treatment Efficacy Tracking
CREATE TABLE treatment_efficacy (
    id INT PRIMARY KEY AUTO_INCREMENT,
    therapy_program_id INT,
    intervention_type VARCHAR(100),
    condition_treated ENUM('depression', 'anxiety', 'ptsd', 'substance_abuse', 'other') NOT NULL,
    sample_size INT,
    baseline_severity_avg FLOAT,
    post_treatment_severity_avg FLOAT,
    improvement_percentage FLOAT,
    symptom_remission_rate FLOAT,
    user_satisfaction_avg FLOAT,
    recurrence_rate_6months FLOAT,
    efficacy_score FLOAT COMMENT 'Composite score',
    study_period_start DATE,
    study_period_end DATE,
    FOREIGN KEY (therapy_program_id) REFERENCES therapy_programs(id) ON DELETE SET NULL,
    INDEX idx_condition (condition_treated)
);

-- QALY/DALY Calculations
CREATE TABLE health_outcome_metrics (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    calculation_date DATE NOT NULL,
    baseline_health_state FLOAT COMMENT '0-1 scale',
    current_health_state FLOAT,
    qaly_gained FLOAT COMMENT 'Quality Adjusted Life Years',
    daly_averted FLOAT COMMENT 'Disability Adjusted Life Years prevented',
    years_life_expectancy_change FLOAT,
    economic_benefit_usd FLOAT COMMENT 'Estimated economic value',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_date (user_id, calculation_date),
    INDEX idx_metrics_date (calculation_date)
);

-- Research Data Export Logs
CREATE TABLE research_data_exports (
    id INT PRIMARY KEY AUTO_INCREMENT,
    export_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    exported_by_user_id INT,
    export_type ENUM('anonymized_dataset', 'research_study_export', 'academic_publication_data', 'government_report') NOT NULL,
    record_count INT,
    data_filters JSON COMMENT '{"date_range": {"start": "2024-01-01", "end": "2024-12-31"}, "region": "Central"}',
    data_fields_included JSON,
    anonymization_method VARCHAR(100),
    encryption_algorithm VARCHAR(50),
    file_location VARCHAR(500),
    FOREIGN KEY (exported_by_user_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_export_date (export_date)
);

-- ============================================================================
-- 8. INTEGRATION ECOSYSTEM TABLES
-- ============================================================================

-- External System Integrations
CREATE TABLE integrations_config (
    id INT PRIMARY KEY AUTO_INCREMENT,
    integration_type ENUM('ehr', 'wearable', 'pharmacy', 'insurance', 'payment_gateway', 'messaging', 'hospital') NOT NULL,
    provider_name VARCHAR(255) NOT NULL,
    api_endpoint VARCHAR(500),
    api_key_encrypted VARCHAR(500),
    is_active BOOLEAN DEFAULT FALSE,
    authentication_method ENUM('oauth2', 'api_key', 'basic_auth', 'jwt') DEFAULT 'api_key',
    webhook_url VARCHAR(500),
    last_sync_timestamp TIMESTAMP,
    sync_frequency_minutes INT DEFAULT 60,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_provider (integration_type, provider_name)
);

-- EHR Patient Records (Cached)
CREATE TABLE ehr_patient_records (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL UNIQUE,
    ehr_patient_id VARCHAR(255),
    hospital_name VARCHAR(255),
    current_medications JSON,
    medical_conditions JSON,
    recent_lab_results JSON,
    blood_type VARCHAR(10),
    allergies TEXT,
    emergency_procedures JSON,
    last_synced TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_hospital (hospital_name)
);

-- Wearable Device Integrations
CREATE TABLE wearable_integrations (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    device_type ENUM('apple_watch', 'fitbit', 'garmin', 'oura_ring', 'polar', 'whoop') NOT NULL,
    device_name VARCHAR(255),
    external_user_id VARCHAR(255) COMMENT 'ID on wearable platform',
    oauth_token_encrypted VARCHAR(500),
    is_connected BOOLEAN DEFAULT TRUE,
    last_sync TIMESTAMP,
    connected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_device_user (device_type, user_id)
);

-- Wearable Data Syncs
CREATE TABLE wearable_data (
    id INT PRIMARY KEY AUTO_INCREMENT,
    wearable_id INT NOT NULL,
    data_date DATE NOT NULL,
    metric_type ENUM('heart_rate', 'heart_rate_variability', 'sleep', 'activity', 'stress_level', 'temperature', 'blood_oxygen') NOT NULL,
    metric_value FLOAT,
    metric_unit VARCHAR(50),
    data_points JSON COMMENT 'Raw data from device',
    synced_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (wearable_id) REFERENCES wearable_integrations(id) ON DELETE CASCADE,
    INDEX idx_user_date (wearable_id, data_date),
    INDEX idx_metric_type (metric_type)
);

-- Pharmacy Integration
CREATE TABLE pharmacy_integrations (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    pharmacy_provider VARCHAR(255),
    pharmacy_id VARCHAR(255),
    active_prescriptions JSON,
    refill_history JSON,
    medication_adherence_score FLOAT,
    last_refill_date DATE,
    next_refill_due DATE,
    last_synced TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_pharmacy (user_id)
);

-- Insurance Integration
CREATE TABLE insurance_integrations (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    insurance_provider VARCHAR(255),
    policy_number VARCHAR(255) ENCRYPTED,
    coverage_type ENUM('mental_health', 'full_coverage', 'limited', 'self_pay') DEFAULT 'limited',
    active_coverage BOOLEAN DEFAULT TRUE,
    copay_amount FLOAT,
    deductible FLOAT,
    max_annual_benefit FLOAT,
    covered_services JSON COMMENT 'List of covered service types',
    authorization_status VARCHAR(50),
    last_verified TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_insurance (user_id)
);

-- ============================================================================
-- 9. SECURITY & COMPLIANCE TABLES
-- ============================================================================

-- Comprehensive Audit Log
CREATE TABLE audit_logs (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    action_type ENUM('login', 'logout', 'data_access', 'data_modification', 'data_deletion', 'file_download', 'report_generation', 'permission_change', 'encryption_key_rotation', 'compliance_check') NOT NULL,
    resource_type VARCHAR(100) COMMENT 'e.g., assessment, chat, user_profile',
    resource_id INT,
    old_value JSON,
    new_value JSON,
    ip_address VARCHAR(45),
    user_agent TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_user_action (user_id, action_type, timestamp),
    INDEX idx_resource (resource_type, resource_id),
    INDEX idx_timestamp (timestamp DESC)
);

-- HIPAA Compliance Checks
CREATE TABLE compliance_checks (
    id INT PRIMARY KEY AUTO_INCREMENT,
    check_type ENUM('hipaa_breach_scan', 'gdpr_audit', 'popia_compliance', 'data_retention_audit', 'encryption_verification', 'access_control_audit') NOT NULL,
    check_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('passed', 'failed', 'warning', 'pending') DEFAULT 'pending',
    findings JSON COMMENT 'Detailed findings',
    remediation_steps TEXT,
    completed_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_check_date (check_date DESC)
);

-- Data Retention Policy Tracking
CREATE TABLE data_retention_tracking (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    data_type ENUM('personal_data', 'health_records', 'chat_history', 'voice_recordings', 'payment_info', 'biometric_data') NOT NULL,
    data_created_date DATE,
    retention_end_date DATE NOT NULL,
    status ENUM('active', 'marked_for_deletion', 'deleted', 'archived') DEFAULT 'active',
    deletion_reason VARCHAR(255),
    deleted_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_retention_end (retention_end_date),
    INDEX idx_status (status)
);

-- User Privacy Settings
CREATE TABLE privacy_settings (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL UNIQUE,
    data_collection_consent BOOLEAN DEFAULT TRUE,
    research_participation_consent BOOLEAN DEFAULT FALSE,
    third_party_sharing_consent BOOLEAN DEFAULT FALSE,
    marketing_communications_consent BOOLEAN DEFAULT FALSE,
    biometric_data_consent BOOLEAN DEFAULT FALSE,
    location_tracking_consent BOOLEAN DEFAULT FALSE,
    wearable_data_consent BOOLEAN DEFAULT FALSE,
    automated_decision_making_consent BOOLEAN DEFAULT FALSE,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user (user_id)
);

-- Zero-Knowledge Proof Authentication
CREATE TABLE zkp_auth_challenges (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    challenge_hash VARCHAR(255),
    response_hash VARCHAR(255),
    attempt_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_valid BOOLEAN,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_auth (user_id, attempt_timestamp)
);

-- Encryption Key Management
CREATE TABLE encryption_keys (
    id INT PRIMARY KEY AUTO_INCREMENT,
    key_id VARCHAR(255) UNIQUE NOT NULL,
    algorithm VARCHAR(50) COMMENT 'AES-256, RSA-2048, etc.',
    key_material_encrypted LONGBLOB,
    key_status ENUM('active', 'rotating', 'archived', 'compromised') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    rotation_scheduled TIMESTAMP,
    rotated_at TIMESTAMP,
    FOREIGN KEY (rotated_from_key_id) REFERENCES encryption_keys(id) ON DELETE SET NULL,
    INDEX idx_key_status (key_status),
    INDEX idx_rotation (rotation_scheduled)
);

-- Federated Learning Model Updates
CREATE TABLE federated_learning_models (
    id INT PRIMARY KEY AUTO_INCREMENT,
    model_type ENUM('risk_predictor', 'sentiment_analyzer', 'crisis_detector', 'voice_emotion', 'relapse_predictor') NOT NULL,
    model_version VARCHAR(50),
    global_model_hash VARCHAR(255),
    aggregation_round INT,
    participants_count INT,
    accuracy_global FLOAT,
    accuracy_local_avg FLOAT,
    privacy_epsilon FLOAT COMMENT 'Differential privacy parameter',
    last_aggregation TIMESTAMP,
    next_aggregation_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_model_type (model_type, model_version)
);

-- ============================================================================
-- 10. TELEPSYCHIATRY & ADAPTIVE COMMUNICATION TABLES
-- ============================================================================

-- Telepsychiatry Session Preparation
CREATE TABLE telepsych_session_prep (
    id INT PRIMARY KEY AUTO_INCREMENT,
    scheduled_session_id INT NOT NULL,
    user_id INT NOT NULL,
    psychiatrist_id INT NOT NULL,
    context_summary TEXT COMMENT 'AI-generated patient context',
    recent_symptoms JSON,
    medication_review JSON,
    suggested_diagnoses JSON COMMENT 'AI suggestions (not final diagnosis)',
    interaction_history_summary TEXT,
    prep_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (psychiatrist_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_session_prep (scheduled_session_id)
);

-- AI Session Co-Pilot Notes
CREATE TABLE session_copilot_notes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    session_id INT NOT NULL,
    counselor_id INT NOT NULL,
    ai_generated_notes TEXT,
    suggested_interventions JSON,
    risk_alerts JSON,
    medication_recommendation_alerts JSON,
    follow_up_suggestions JSON,
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    counselor_reviewed_at TIMESTAMP,
    is_adopted BOOLEAN,
    FOREIGN KEY (counselor_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_session_notes (session_id)
);

-- Prescription Tracking
CREATE TABLE prescription_tracking (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    psychiatrist_id INT NOT NULL,
    medication_name VARCHAR(255),
    dosage VARCHAR(100),
    frequency VARCHAR(100),
    prescribed_date DATE,
    prescribed_by_professional VARCHAR(100),
    effectiveness_rating INT COMMENT '1-10',
    side_effects TEXT,
    adherence_score FLOAT,
    last_refill_date DATE,
    next_refill_date DATE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (psychiatrist_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_medications (user_id)
);

-- Multi-Channel Message Queue
CREATE TABLE message_queue (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    message_type ENUM('sms', 'email', 'push', 'whatsapp', 'telegram', 'in_app') NOT NULL,
    channel_identifier VARCHAR(255) COMMENT 'Phone, email, or app device ID',
    content TEXT,
    priority ENUM('low', 'normal', 'high', 'urgent') DEFAULT 'normal',
    status ENUM('queued', 'sent', 'delivered', 'failed', 'bounced') DEFAULT 'queued',
    attempts INT DEFAULT 0,
    max_attempts INT DEFAULT 3,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sent_at TIMESTAMP,
    delivery_timestamp TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_channel (user_id, message_type),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at DESC)
);

-- ============================================================================
-- 11. ECONOMIC SUSTAINABILITY TABLES
-- ============================================================================

-- Dynamic Pricing Configuration
CREATE TABLE dynamic_pricing_rules (
    id INT PRIMARY KEY AUTO_INCREMENT,
    service_type ENUM('counselor_session', 'therapy_program', 'assessment', 'group_session', 'consultation') NOT NULL,
    base_price_usd FLOAT,
    pricing_model ENUM('fixed', 'sliding_scale', 'income_based', 'usage_based', 'subscription') DEFAULT 'fixed',
    rules_json JSON COMMENT 'Dynamic pricing rules config',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- User Pricing Tiers
CREATE TABLE user_pricing_tiers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL UNIQUE,
    self_reported_income_level ENUM('very_low', 'low', 'medium', 'high', 'prefer_not_to_say') DEFAULT 'prefer_not_to_say',
    employment_status ENUM('unemployed', 'part_time', 'full_time', 'student', 'other') DEFAULT 'other',
    household_size INT,
    calculated_affordability_score FLOAT COMMENT '0-1 scale for determining discounts',
    applied_discount_percentage FLOAT DEFAULT 0,
    price_per_session_usd FLOAT,
    last_recalculated TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_affordability (calculated_affordability_score)
);

-- Micro-Insurance Products
CREATE TABLE micro_insurance_products (
    id INT PRIMARY KEY AUTO_INCREMENT,
    product_name VARCHAR(255),
    description TEXT,
    coverage_type ENUM('crisis_sessions', 'hospitalization', 'medication', 'comprehensive') DEFAULT 'crisis_sessions',
    premium_usd_monthly FLOAT,
    max_claims_per_month INT,
    max_benefit_usd_per_claim FLOAT,
    deductible_usd FLOAT,
    is_active BOOLEAN DEFAULT TRUE
);

-- User Insurance Subscriptions
CREATE TABLE user_insurance_subscriptions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    insurance_product_id INT NOT NULL,
    subscription_status ENUM('active', 'paused', 'cancelled') DEFAULT 'active',
    start_date DATE,
    end_date DATE,
    monthly_premium_usd FLOAT,
    total_claims_filed INT DEFAULT 0,
    total_claims_paid_usd FLOAT DEFAULT 0,
    last_claim_date DATE,
    auto_renew BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (insurance_product_id) REFERENCES micro_insurance_products(id) ON DELETE RESTRICT,
    INDEX idx_user_insurance (user_id, subscription_status)
);

-- Payment Processing
CREATE TABLE payment_transactions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    amount_usd FLOAT NOT NULL,
    currency VARCHAR(10) DEFAULT 'USD',
    payment_method ENUM('mpesa', 'mtn_money', 'airtel_money', 'creditcard', 'bank_transfer', 'insurance', 'voucher') NOT NULL,
    payment_status ENUM('pending', 'completed', 'failed', 'refunded', 'cancelled') DEFAULT 'pending',
    transaction_id VARCHAR(255),
    reference_number VARCHAR(255),
    service_type VARCHAR(100),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_transactions (user_id, created_at),
    INDEX idx_status (payment_status)
);

-- Donor & Impact Tracking
CREATE TABLE impact_metrics_for_donors (
    id INT PRIMARY KEY AUTO_INCREMENT,
    reporting_period_start DATE,
    reporting_period_end DATE,
    total_users_served INT,
    crisis_interventions_count INT,
    lives_saved_estimate INT,
    qaly_generated FLOAT,
    daly_prevented FLOAT,
    economic_value_created_usd FLOAT,
    cost_per_user_helped_usd FLOAT,
    user_satisfaction_score FLOAT,
    roi_percentage FLOAT COMMENT 'Return on investment for donors',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- INDEXES FOR PERFORMANCE OPTIMIZATION
-- ============================================================================

-- Indexes already created inline with table definitions above.
-- Additional composite indexes for common queries:

CREATE INDEX idx_user_recent_activity ON users(id, last_login);
CREATE INDEX idx_assessment_timeline ON assessments(user_id, created_at DESC);
CREATE INDEX idx_chat_timeline ON chat_messages(chat_id, created_at DESC);
CREATE INDEX idx_crisis_response_time ON crisis_alerts_advanced(created_at DESC, response_status);
