# TALK 2 ME - Database Schema Documentation

## Overview
This document describes the complete database schema for the TALK 2 ME mental health support system. The database is designed to support user management, mental health assessments, real-time chat, crisis detection, counselling sessions, payment processing, and comprehensive analytics.

---

## Database Architecture

### Key Design Principles
1. **Referential Integrity**: Foreign keys enforce data consistency
2. **Scalability**: Proper indexing for quick query performance
3. **Audit Trail**: All changes tracked for compliance and debugging
4. **Data Security**: Sensitive data properly segregated
5. **Flexibility**: JSON columns for semi-structured data
6. **GDPR Compliance**: Data retention policies and user privacy controls

---

## 1. USER MANAGEMENT TABLES

### `users`
**Purpose**: Core user account information
**Key Fields**:
- `id`: Primary key
- `account_type`: User, Counsellor, or Admin
- `is_verified`: Email verification status
- `last_login`: Track user activity
- `language_preference`: For multilingual support

**Indexes**: username, email, account_type

```
Relationships:
├── UserProfile (1:1)
├── LoginHistory (1:N)
├── PasswordResetToken (1:N)
├── EmailVerificationToken (1:N)
├── Assessments (1:N)
├── ChatConversations (1:N)
├── CounsellingSession (1:N - as user)
├── Payments (1:N)
├── Subscriptions (1:N)
├── Notifications (1:N)
├── CrisisAlerts (1:N)
└── Resources (1:N - via ResourceViews)
```

### `user_profiles`
**Purpose**: Extended user information and preferences
**Key Fields**:
- `emergency_contact_*`: Emergency contact details
- `medical_history`: Health background
- `privacy_level`: Public/Private/Friends Only
- `notifications_enabled`: User notification preferences

### `counsellors`
**Purpose**: Professional counsellor information
**Key Fields**:
- `license_number`: Unique license identifier
- `specializations`: Areas of expertise (JSON)
- `hourly_rate`: Session pricing
- `availability_status`: Real-time availability
- `is_verified`: License verification status
- `rating`: Average counsellor rating

---

## 2. AUTHENTICATION & SECURITY TABLES

### `password_reset_tokens`
**Purpose**: Secure password reset functionality
- Token expires after set period
- Single-use tokens

### `email_verification_tokens`
**Purpose**: Email verification during registration

### `login_history`
**Purpose**: Track all login attempts for security
**Key Fields**:
- `ip_address`: Source IP
- `user_agent`: Browser/device info
- `device_type`: Mobile, Desktop, Tablet

---

## 3. ASSESSMENT TABLES

### `assessment_types`
**Purpose**: Define available mental health assessments
**Examples**:
- GAD7 (Generalized Anxiety Disorder)
- PHQ9 (Patient Health Questionnaire)
- K10 (Kessler Psychological Distress Scale)

**Key Fields**:
- `total_questions`: Number of questions
- `min_score`, `max_score`: Score range
- `language`: Support multiple languages

### `assessments`
**Purpose**: Store user assessment responses
**Key Fields**:
- `responses`: JSON object with question-answer pairs
- `total_score`: Calculated score
- `risk_level`: Low/Moderate/High/Severe
- `interpretation`: AI-generated interpretation
- `recommendations`: Personalized recommendations

### `assessment_progress`
**Purpose**: Track improvement over time
**Key Fields**:
- `score_change`: Numerical difference
- `improvement_percentage`: % change
- `trend`: Improving/Declining/Stable

---

## 4. CHAT & MESSAGING TABLES

### `chat_conversations`
**Purpose**: Group messages into conversations
**Types**:
- User-AI: Conversations with AI support
- User-Counsellor: Direct counsellor communication
- Group: Group support sessions

**Key Fields**:
- `conversation_type`: Type of conversation
- `status`: Active/Closed/Archived
- `total_messages`: Denormalized for quick stats

### `chat_messages`
**Purpose**: Individual chat messages with AI analysis
**Key Fields**:
- `sender_type`: User/Counsellor/AI
- `sentiment_score`: AI-detected sentiment (-1 to 1)
- `sentiment_label`: Positive/Neutral/Negative
- `crisis_detected`: Boolean flag for crisis keywords
- `crisis_keywords`: JSON array of detected keywords
- `is_read`: Message read status

**Indexes**: conversation_id, sender_id, created_at, crisis_detected

### `message_reactions`
**Purpose**: Emoji reactions on messages (like buttons)

---

## 5. CRISIS MANAGEMENT TABLES

### `crisis_alerts`
**Purpose**: Flag and track crisis situations
**Severity Levels**:
- Low: Casual mention
- Medium: Concerning pattern
- High: Explicit crisis language
- Critical: Immediate danger

**Key Fields**:
- `alert_type`: Keyword Detection/Manual Report/Pattern Detection
- `status`: Active/In Review/Resolved/False Alarm
- `assigned_to`: Counsellor responsible
- `reviewed_by`: Admin who reviewed

### `emergency_resources`
**Purpose**: Directory of crisis hotlines and resources
**Fields**:
- `available_24_7`: Boolean for urgent access
- `languages_supported`: JSON array
- `is_verified`: Verified by admins
- Geographic indexing for location-based search

---

## 6. COUNSELLING TABLES

### `counselling_sessions`
**Purpose**: Track all counselling sessions
**Session Types**:
- Individual: One-on-one
- Group: Multiple users
- Crisis: Emergency intervention

**Communication Methods**: Chat/Voice/Video

**Key Fields**:
- `scheduled_at`: Appointment time
- `duration_minutes`: Session length
- `status`: Scheduled/In Progress/Completed/Cancelled/No-show
- `payment_status`: Pending/Paid/Refunded
- `follow_up_required`: Boolean for required follow-up

### `session_notes`
**Purpose**: Detailed clinical notes (1:1 with session)
**Key Fields**:
- `clinical_notes`: Observations
- `diagnosis_notes`: Assessment findings
- `treatment_plan`: Next steps
- `medications_prescribed`: Any prescriptions
- `referrals`: External referrals

---

## 7. RESOURCES & CONTENT TABLES

### `resources`
**Purpose**: Educational content library
**Content Types**:
- Article: Text-based
- Video: Embedded videos
- Audio: Podcasts/recordings
- Document: PDF/downloadables
- Interactive: Interactive tools

**Key Fields**:
- `category`/`subcategory`: Content organization
- `tags`: JSON array for filtering
- `difficulty_level`: Beginner/Intermediate/Advanced
- `estimated_read_time_minutes`: Time estimate
- `view_count`: Popularity tracking
- `rating`: Average user rating

### `resource_views`
**Purpose**: Track resource engagement
**Key Fields**:
- `time_spent_seconds`: User engagement metric
- `completed`: Boolean for completion
- `user_id`: NULL for anonymous views

### `resource_ratings`
**Purpose**: User reviews and ratings
**Key Fields**:
- `rating`: 1-5 stars
- `review_text`: Written review
- `helpful_count`: Upvotes on review

---

## 8. PAYMENT & SUBSCRIPTION TABLES

### `payments`
**Purpose**: Track all financial transactions
**Transaction Types**:
- Session: Paid counselling sessions
- Subscription: Plan renewal
- Resource Purchase: Premium content
- Donation: User donations

**Payment Methods**: Credit Card/Debit/Mobile Money/Bank Transfer/PayPal

**Key Fields**:
- `payment_gateway`: Stripe/PayPal/etc.
- `transaction_id`: External payment ID
- `status`: Pending/Completed/Failed/Refunded/Cancelled
- `receipt_url`: Digital receipt

### `subscriptions`
**Purpose**: User subscription plans
**Plan Types**:
- Free: Basic access
- Basic: Limited sessions
- Professional: Counsellor access
- Premium: Unlimited access

**Key Fields**:
- `sessions_limit`/`sessions_used`: Track usage
- `storage_limit_gb`/`storage_used_gb`: File storage
- `features`: JSON array of enabled features
- `auto_renew`: Automatic billing

---

## 9. NOTIFICATION TABLES

### `notifications`
**Purpose**: In-app notifications
**Types**: Message/Session/Alert/Resource/System

**Priority Levels**: Low/Medium/High/Critical

### `sms_log`
**Purpose**: SMS message history
**Status**: Pending/Sent/Failed/Delivered

### `email_log`
**Purpose**: Email communication history
**Statuses**: Pending/Sent/Failed/Bounced

---

## 10. ANALYTICS & REPORTING TABLES

### `user_analytics`
**Purpose**: Daily user engagement metrics
**Tracked Metrics**:
- `total_sessions`: Count of sessions
- `total_messages`: Message count
- `assessments_completed`: Assessment count
- `resources_viewed`: Resources accessed
- `average_sentiment_score`: Overall sentiment trend
- `crisis_incidents`: Crisis event count
- `engagement_score`: Calculated engagement metric
- `last_active_date`: Last activity timestamp

**Indexed on**: user_id, tracked_date

### `system_analytics`
**Purpose**: Platform-wide daily statistics
**Metrics**:
- `total_active_users`: Daily active users
- `new_users_today`: New registrations
- `crisis_alerts_today`: Crisis event count
- `average_session_duration_minutes`: Average session length
- `server_uptime_percentage`: System availability
- `error_count`: Error tracking

### `ai_model_performance`
**Purpose**: Track ML model metrics
**Metrics**: Accuracy/Precision/Recall/F1-Score

---

## 11. ADMIN & MODERATION TABLES

### `admin_actions_log`
**Purpose**: Audit trail for administrative actions
**Logged Actions**:
- User management
- Content moderation
- System configuration changes
- Crisis resolution actions

**Key Fields**:
- `action_type`: Type of action
- `entity_type`/`entity_id`: What was modified
- `old_value`/`new_value`: Before/after states
- `ip_address`: Action source

### `content_moderation`
**Purpose**: Flag and review reported content
**Reasons**: Spam/Offensive/Misinformation/Harmful/Other

**Statuses**: Reported/Under Review/Approved/Rejected/Deleted

### `user_report`
**Purpose**: Track user-to-user reports
**Report Types**: Harassment/Abuse/Spam/Impersonation/Other

---

## 12. SYSTEM CONFIGURATION TABLES

### `system_settings`
**Purpose**: Application configuration
**Examples**:
```
maintenance_mode: true
max_chat_history_days: 90
crisis_alert_threshold: 0.8
```

### `feature_flags`
**Purpose**: Feature toggle management
**Key Fields**:
- `rollout_percentage`: Gradual rollout (0-100)
- `is_enabled`: Enable/disable feature

---

## 13. AUDIT TRAIL TABLES

### `audit_trail`
**Purpose**: Complete change history for compliance
**Operations**: INSERT/UPDATE/DELETE
**Key Fields**:
- `old_data`/`new_data`: JSON snapshots
- `changed_by`: User making change
- `change_reason`: Reason for modification

### `data_retention_policies`
**Purpose**: Define data lifecycle
**Examples**:
- Delete chat messages after 2 years
- Delete login history after 1 year
- Archive assessments after 3 years

---

## 14. SUPPORT & FEEDBACK TABLES

### `user_feedback`
**Purpose**: Feature requests and issue reports
**Types**: Bug Report/Feature Request/Improvement/General Feedback

### `support_tickets`
**Purpose**: Customer support request management
**Statuses**: Open/In Progress/Waiting for User/Resolved/Closed

**Priorities**: Low/Medium/High/Critical

### `support_ticket_responses`
**Purpose**: Communication on support tickets
**Enables**: Multi-message support conversations

---

## 15. TRANSLATION TABLES

### `supported_languages`
**Purpose**: Define supported languages
**Key Fields**:
- `language_code`: ISO 639-1 (e.g., 'en', 'lg')
- `native_speakers`: Total speakers (stats)

### `translations`
**Purpose**: Store translated strings
**Key Fields**:
- `translation_key`: Reference ID (e.g., 'btn_submit')
- `translation_value`: Translated text
- `context`: Where used (e.g., 'registration')
- `is_reviewed`: Quality control flag

---

## Database Optimization

### Key Indexes Created
```sql
-- Performance indexes
idx_email, idx_username, idx_account_type on users
idx_user_id on chat_conversations, assessments, payments
idx_crisis_detected on chat_messages
idx_status on crisis_alerts, sessions, support_tickets
idx_created_at on notifications, login_history
idx_language_code on translations
```

### Query Optimization Patterns

**Get user's recent conversations:**
```sql
SELECT * FROM chat_conversations 
WHERE user_id = ? 
ORDER BY updated_at DESC 
LIMIT 10;
```

**Find active crisis alerts:**
```sql
SELECT * FROM crisis_alerts 
WHERE status = 'Active' 
AND severity IN ('High', 'Critical')
ORDER BY created_at ASC;
```

**Calculate user engagement:**
```sql
SELECT user_id, 
  COUNT(DISTINCT assessment_id) as assessments,
  COUNT(DISTINCT session_id) as sessions
FROM user_analytics
WHERE tracked_date >= DATE_SUB(NOW(), INTERVAL 30 DAY)
GROUP BY user_id;
```

---

## Migration Guide

### Initial Setup
1. Create all tables in order of dependencies
2. Add foreign keys
3. Create indexes
4. Insert system data (languages, assessment types, resources)

### Adding New Features
1. Create new tables following naming conventions
2. Add appropriate indexes
3. Update ORM models
4. Create migration script
5. Test referential integrity

---

## Backup & Recovery

### Recommended Backup Strategy
- **Full backup**: Daily at 2 AM UTC
- **Incremental backup**: Every 6 hours
- **Retention**: 30 days for daily, 90 days for weekly
- **Disaster recovery**: Test restore monthly

### Critical Tables for Backup
1. `users` - Core data
2. `chat_messages` - User conversations
3. `assessments` - Health data
4. `payments` - Financial records
5. `crisis_alerts` - Safety critical

---

## Data Privacy & Compliance

### GDPR Compliance
- User right to access: Query user's data easily
- Right to deletion: CASCADE deletes remove all user data
- Data retention: Defined in data_retention_policies
- Audit trail: Complete change history

### Data Categories
- **PII (Personally Identifiable)**: user, user_profiles
- **Health Data**: assessments, counselling_sessions
- **Financial**: payments, subscriptions
- **Communications**: chat_messages, email_log
- **Sensitive**: crisis_alerts, session_notes

### Encryption Recommendations
- At rest: Database-level encryption
- In transit: TLS/SSL for all connections
- Sensitive fields: Hash passwords, encrypt SSNs

---

## Performance Metrics

### Expected Throughput
- **Chat messages**: 10,000/hour
- **Assessments**: 1,000/day
- **Concurrent users**: 5,000
- **Query response time**: <200ms (95th percentile)

### Scaling Considerations
- Partitioning: Messages by date after 1GB
- Caching: Redis for frequently accessed data
- Read replicas: For analytics queries
- Archive: Move old data to separate DB

---

## Integration Points

### External Services
- **Payment Gateway**: Stripe/PayPal - references in `payments`
- **SMS Service**: Twilio - logs in `sms_log`
- **Email Service**: SendGrid - logs in `email_log`
- **Cloud Storage**: S3/Firebase - URLs in various tables

---

## Support & Maintenance

### Regular Maintenance Tasks
- Daily: Check error logs, monitoring alerts
- Weekly: Vacuum/optimize indexes
- Monthly: Review slow queries, test backups
- Quarterly: Analyze growth, plan scaling
- Annually: Full security audit

### Key Metrics to Monitor
- Database size growth
- Slow query count
- Backup success rate
- Replication lag
- Connection pool usage
