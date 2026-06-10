# TALK 2 ME Database Setup Guide

## Quick Start

### 1. Database Requirements

**Supported Databases:**
- MySQL 8.0+ (Recommended for production)
- PostgreSQL 12+
- SQLite 3 (Development only)
- MariaDB 10.3+

**Minimum Specifications:**
- Storage: 10 GB initial
- RAM: 4 GB minimum
- Connections: 100 concurrent connections
- Character Set: UTF-8MB4 (for emoji support)

---

## Installation & Configuration

### Option 1: MySQL (Production Recommended)

#### Install MySQL

**Windows:**
```bash
# Using Chocolatey
choco install mysql

# Or download from https://dev.mysql.com/downloads/mysql/
```

**macOS:**
```bash
# Using Homebrew
brew install mysql
brew services start mysql
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install mysql-server
sudo mysql_secure_installation
sudo systemctl start mysql
```

#### Create Database and User

```bash
# Connect to MySQL
mysql -u root -p

# Run these SQL commands
CREATE DATABASE talk2me CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'talk2me_user'@'localhost' IDENTIFIED BY 'secure_password_here';
GRANT ALL PRIVILEGES ON talk2me.* TO 'talk2me_user'@'localhost';
GRANT ALL PRIVILEGES ON talk2me_test.* TO 'talk2me_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

#### Verify Installation

```bash
mysql -u talk2me_user -p talk2me -e "SELECT VERSION();"
```

---

### Option 2: PostgreSQL

#### Install PostgreSQL

**Windows:**
```bash
# Download from https://www.postgresql.org/download/windows/
# Run installer and follow instructions
```

**macOS:**
```bash
brew install postgresql@15
brew services start postgresql@15
```

**Linux (Ubuntu):**
```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
sudo systemctl start postgresql
```

#### Create Database and User

```bash
# Connect as postgres user
sudo -u postgres psql

# Run these SQL commands
CREATE DATABASE talk2me;
CREATE USER talk2me_user WITH PASSWORD 'secure_password_here';
GRANT ALL PRIVILEGES ON DATABASE talk2me TO talk2me_user;
ALTER ROLE talk2me_user WITH LOGIN;
\q
```

---

### Option 3: SQLite (Development Only)

SQLite requires no installation - it's built into Python!

---

## Environment Configuration

### 1. Create .env file

Create `backend/.env`:

```bash
# Database Configuration
DATABASE_URL=mysql+pymysql://talk2me_user:secure_password_here@localhost:3306/talk2me

# Alternative for PostgreSQL
# DATABASE_URL=postgresql://talk2me_user:secure_password_here@localhost:5432/talk2me

# Alternative for SQLite (development)
# DATABASE_URL=sqlite:///./talk2me.db

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-very-secret-key-change-this-in-production

# Database Connection Pool
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20
DB_POOL_RECYCLE=3600

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/talk2me.log

# Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_USE_TLS=True
MAIL_DEFAULT_SENDER=noreply@talk2me.com

# SMS Configuration (Twilio)
TWILIO_ACCOUNT_SID=your-twilio-sid
TWILIO_AUTH_TOKEN=your-twilio-token
TWILIO_PHONE_NUMBER=+1234567890

# Payment Configuration (Stripe)
STRIPE_PUBLIC_KEY=pk_test_your_key
STRIPE_SECRET_KEY=sk_test_your_key

# AI/ML Configuration
CRISIS_DETECTION_MODEL_PATH=ml_models/trained_models/crisis_detector.pkl
SENTIMENT_MODEL_PATH=ml_models/trained_models/sentiment_model.pkl
LUGANDA_NLP_MODEL_PATH=ml_models/trained_models/luganda_nlp.pkl

# Security
JWT_SECRET_KEY=your-jwt-secret-change-this
JWT_ALGORITHM=HS256
TOKEN_EXPIRY_HOURS=24

# Session Configuration
SESSION_LIFETIME_MINUTES=30
MAX_SESSIONS_PER_DAY=10

# Crisis Detection
CRISIS_DETECTION_THRESHOLD=0.75
CRISIS_ALERT_EMAIL=crisis@talk2me.com
CRISIS_RESPONSE_TIMEOUT_MINUTES=15

# Sentry (Error Tracking)
SENTRY_DSN=your-sentry-dsn-url
```

### 2. Create .env.test for Testing

Create `backend/.env.test`:

```bash
DATABASE_URL=sqlite:///:memory:
FLASK_ENV=testing
FLASK_DEBUG=False
SECRET_KEY=test-secret-key
JWT_SECRET_KEY=test-jwt-secret
```

---

## Python Dependencies

### Install Required Packages

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Additional packages for database
pip install pymysql  # For MySQL
# OR
pip install psycopg2-binary  # For PostgreSQL
```

### Update requirements.txt

Add/ensure these packages are in `backend/requirements.txt`:

```txt
Flask==2.3.2
SQLAlchemy==2.0.19
pymysql==1.1.0
psycopg2-binary==2.9.7
python-dotenv==1.0.0
flask-sqlalchemy==3.0.5
flask-migrate==4.0.4
python-dateutil==2.8.2
marshmallow==3.19.0
marshmallow-sqlalchemy==0.29.0
```

---

## Database Initialization

### Method 1: Using Python Script

```bash
# From backend directory with virtual environment activated
python db_manager.py --init
```

### Method 2: Using Flask-Migrate (Alembic)

```bash
# Initialize migrations
flask db init

# Create initial migration
flask db migrate -m "Initial migration"

# Apply migration
flask db upgrade
```

### Method 3: Manual SQL

```bash
# Import the SQL schema
mysql -u talk2me_user -p talk2me < database_schema.sql
```

---

## Configuration in Flask App

### Update config.py

```python
import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'mysql+pymysql://talk2me_user:password@localhost/talk2me'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': int(os.getenv('DB_POOL_SIZE', 10)),
        'pool_recycle': int(os.getenv('DB_POOL_RECYCLE', 3600)),
        'pool_pre_ping': True,
        'max_overflow': int(os.getenv('DB_MAX_OVERFLOW', 20)),
    }
    
    # Session configuration
    PERMANENT_SESSION_LIFETIME = timedelta(
        minutes=int(os.getenv('SESSION_LIFETIME_MINUTES', 30))
    )
    
    # Security
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev-jwt-secret')
    JWT_ALGORITHM = 'HS256'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        hours=int(os.getenv('TOKEN_EXPIRY_HOURS', 24))
    )

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    SQLALCHEMY_ECHO = True

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False

config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
```

### Update app/__init__.py

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config_by_name
import os

db = SQLAlchemy()

def create_app(config_name='development'):
    app = Flask(__name__)
    
    # Load configuration
    config = config_by_name.get(config_name, config_by_name['development'])
    app.config.from_object(config)
    
    # Initialize database
    db.init_app(app)
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    # Register blueprints
    from app.routes import auth, chat, assessment, counselling
    app.register_blueprint(auth.bp)
    app.register_blueprint(chat.bp)
    app.register_blueprint(assessment.bp)
    app.register_blueprint(counselling.bp)
    
    return app
```

---

## Verify Installation

### 1. Test Database Connection

```python
# Run from backend directory
from app import create_app, db

app = create_app()
with app.app_context():
    try:
        db.session.execute("SELECT 1")
        print("✓ Database connection successful!")
    except Exception as e:
        print(f"✗ Connection failed: {e}")
```

### 2. Check Tables

```bash
# For MySQL
mysql -u talk2me_user -p talk2me -e "SHOW TABLES;"

# For PostgreSQL
psql -U talk2me_user -d talk2me -c "\dt"
```

### 3. Run Sample Query

```python
from app import create_app, db
from app.models.db_models import User

app = create_app()
with app.app_context():
    user_count = db.session.query(User).count()
    print(f"Total users: {user_count}")
```

---

## Docker Setup (Alternative)

### Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: root_password
      MYSQL_DATABASE: talk2me
      MYSQL_USER: talk2me_user
      MYSQL_PASSWORD: secure_password
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      timeout: 20s
      retries: 10

  phpmyadmin:
    image: phpmyadmin:latest
    environment:
      PMA_HOST: mysql
      PMA_USER: talk2me_user
      PMA_PASSWORD: secure_password
    ports:
      - "8080:80"
    depends_on:
      - mysql

  backend:
    build: ./backend
    environment:
      DATABASE_URL: mysql+pymysql://talk2me_user:secure_password@mysql:3306/talk2me
    ports:
      - "5000:5000"
    depends_on:
      - mysql
    volumes:
      - ./backend:/app

volumes:
  mysql_data:
```

### Run Docker Setup

```bash
# Build and start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

---

## Backup & Recovery

### Automated Backups

```bash
#!/bin/bash
# backup_database.sh

BACKUP_DIR="./backups"
DATE=$(date +%Y%m%d_%H%M%S)
DATABASE="talk2me"
USER="talk2me_user"

mkdir -p $BACKUP_DIR

# MySQL backup
mysqldump -u $USER -p $DATABASE > $BACKUP_DIR/backup_$DATE.sql

# Compress
gzip $BACKUP_DIR/backup_$DATE.sql

echo "Backup completed: $BACKUP_DIR/backup_$DATE.sql.gz"
```

### Restore from Backup

```bash
# MySQL restore
gunzip < backups/backup_YYYYMMDD_HHMMSS.sql.gz | \
  mysql -u talk2me_user -p talk2me
```

---

## Performance Optimization

### 1. Create Indexes

Indexes are created automatically by the schema, but you can verify:

```sql
-- MySQL
SHOW INDEXES FROM users;
SHOW INDEXES FROM chat_messages;
SHOW INDEXES FROM assessments;
```

### 2. Enable Query Caching

For MySQL:

```sql
-- Check query cache
SHOW VARIABLES LIKE 'query_cache%';

-- Enable (if disabled)
SET GLOBAL query_cache_size = 268435456;  -- 256MB
SET GLOBAL query_cache_type = 1;
```

### 3. Connection Pooling

Already configured in `config.py`:
- Pool size: 10 connections
- Max overflow: 20 additional connections
- Pool recycle: 1 hour

### 4. Monitor Performance

```sql
-- Slow query log
SET GLOBAL slow_query_log = 'ON';
SET GLOBAL long_query_time = 2;

-- Check slow queries
SELECT * FROM mysql.slow_log ORDER BY start_time DESC LIMIT 10;
```

---

## Troubleshooting

### Connection Issues

```python
# Debug connection
from sqlalchemy import create_engine, event, pool
import logging

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

engine = create_engine('mysql+pymysql://user:pass@localhost/db', 
                       echo=True, echo_pool=True)
```

### Common Errors

**Error: "No module named 'pymysql'"**
```bash
pip install pymysql
```

**Error: "Access denied for user"**
- Check credentials in .env
- Verify user exists in MySQL
- Check user permissions

**Error: "Database does not exist"**
```bash
mysql -u root -p -e "CREATE DATABASE talk2me;"
```

**Error: "Connection pool overflow"**
- Check for unclosed connections
- Increase pool_size in config.py

---

## Production Deployment

### 1. Security Hardening

```sql
-- Create separate user for app (no SUPER privileges)
CREATE USER 'app_user'@'app_host' IDENTIFIED BY 'strong_password';
GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, 
      INDEX, ALTER ON talk2me.* TO 'app_user'@'app_host';
FLUSH PRIVILEGES;

-- Disable binary logging of sensitive data
SET sql_log_bin = 0;
```

### 2. Enable Replication

```sql
-- Primary server
CHANGE MASTER TO
  MASTER_HOST = 'primary_host',
  MASTER_USER = 'replication_user',
  MASTER_PASSWORD = 'password',
  MASTER_LOG_FILE = 'mysql-bin.000001',
  MASTER_LOG_POS = 0;

START SLAVE;
SHOW SLAVE STATUS\G
```

### 3. Monitoring

Use tools like:
- MySQL Enterprise Monitor
- Percona Monitoring and Management
- DataGrip
- MySQL Workbench

---

## Support & Documentation

- SQL Alchemy: https://docs.sqlalchemy.org/
- MySQL: https://dev.mysql.com/doc/
- PostgreSQL: https://www.postgresql.org/docs/
- Flask-SQLAlchemy: https://flask-sqlalchemy.palletsprojects.com/

---

## Next Steps

1. ✓ Install database system
2. ✓ Create database and user
3. ✓ Configure environment variables
4. ✓ Initialize database schema
5. Seed sample data
6. Run tests
7. Deploy to production

Good luck with TALK 2 ME! 🚀
