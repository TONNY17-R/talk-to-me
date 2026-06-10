# Comprehensive System Report

This document provides a detailed overview of the **Talk to Me** mental health support platform, covering architecture, features, components, development setup, deployment, and operational considerations. It is intended as a comprehensive report for stakeholders, developers, and maintainers.

---

## 1. Project Overview

Talk to Me is a mental health support platform focused on providing accessible assistance to users in Uganda. It integrates AI-powered chat support, professional counselling booking, mental health assessments, crisis detection, and multi-language content.

The system employs a microservice-like backend with a React-based frontend and several machine learning models for natural language processing.

---

## 2. Architecture & Components

### 2.1 Backend
- **Framework:** Flask 2.3.2
- **Database:** PostgreSQL (ORM: SQLAlchemy)
- **Cache:** Redis for session management and rate limiting
- **Authentication:** JWT tokens via PyJWT
- **Email/SMS:** Flask-Mail and Africa's Talking API

#### Key Modules
- `app/models` – database models (users, counsellors, assessments, payments, etc.)
- `app/routes` – API endpoints (auth, chat, assessment, counselling, admin)
- `app/services` – business logic (AI integration, analytics, payments, etc.)
- `app/ai` – wrappers and utilities for AI services

### 2.2 Frontend
- **Framework:** React 18 with Vite
- **State Management:** React Context (Auth, Chat, User, Theme, etc.)
- **Routing:** React Router
- **Communication:** Axios for REST calls, Socket.io for realtime chat
- **Styling:** CSS Modules + global styles

#### Structure
- `components` – reusable UI parts grouped by feature
- `pages` – top-level views (AssessmentPage, ChatPage, AdminPage, etc.)
- `services` – API client wrappers
- `contexts` – providers for global state

### 2.3 Machine Learning
- **Datasets:** crisis_keywords.json, uganda_mental_health.csv, luganda_corpus.txt
- **Models:** various NLP models trained for crisis detection, sentiment analysis, Luganda translation
- **Scripts:** training utilities under `ml_models/training_scripts` including `train_crisis.py`, `train_luganda.py`, `train_sentiment.py`

### 2.4 DevOps & Deployment
- Docker for containerization (backend and frontend Dockerfiles)
- `docker-compose.yml` orchestrates services including PostgreSQL, Redis, and Nginx
- Nginx acts as reverse proxy and serves frontend
- GitHub Actions for CI/CD
- `setup.sh` script for initial environment configuration

### 2.5 Testing
- Backend: `pytest` tests located in `backend/tests`
- Frontend: linting via ESLint (npm run lint)

---

## 3. Security & Compliance
- Passwords hashed with bcrypt
- HTTPS enforced behind Nginx
- Input validation using marshmallow/validators
- Role-based access control for admin endpoints
- Token expiration and refresh handling

---

## 4. API Endpoints
*Summarize in table format (see README for details).*

---

## 5. Database Schema
Outline key tables:
- `users`
- `counsellors`
- `appointments`
- `assessments`
- `chat_sessions`

Provide ER diagram reference if available (not included here).

---

## 6. Installation & Development Setup
(Refer to README but include additional notes for local debugging, environment variables, etc.)

---

## 7. Operational Guide
- Running migrations
- Monitoring logs (docker-compose logs)
- Managing machine learning model updates
- Backups and restoration procedures

---

## 8. Future Enhancements
- Integration with additional languages
- Mobile app version
- Advanced analytics dashboard
- Offline support and PWA features

---

## 9. Appendices
- Data dictionary
- Configuration file templates
- Contact information for support and development team

---

*Generated on March 9, 2026.*
