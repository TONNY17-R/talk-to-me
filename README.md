# Talk to Me - Mental Health Support Platform

A comprehensive mental health support platform for Uganda with AI chatbot, professional counselling, assessments, and resources.

## Features

- **AI Chat Support**: 24/7 AI-powered chat for mental health support
- **Mental Health Assessments**: PHQ-9 and GAD-7 assessments
- **Professional Counselling**: Book sessions with licensed counsellors
- **Resources**: Articles, videos, and exercises for mental wellness
- **Crisis Detection**: Real-time detection and response to crisis indicators
- **Multi-language Support**: English, Luganda, and Swahili
- **Admin Dashboard**: Manage users, resources, and crisis alerts

## Project Structure

```
talk-to-me-uganda/
├── backend/              # Flask backend application
├── frontend/             # React frontend application
├── ml_models/           # Machine learning models and training scripts
├── docker-compose.yml   # Docker Compose configuration
├── Dockerfile.backend   # Backend Docker image
├── Dockerfile.frontend  # Frontend Docker image
├── nginx.conf          # Nginx reverse proxy configuration
├── .github/            # GitHub Actions workflows
└── setup.sh            # Setup script
```

## Tech Stack

### Backend
- Python 3.10
- Flask 2.3.2
- SQLAlchemy ORM
- PostgreSQL
- Redis
- Flask-Mail, Africa's Talking API
- PyJWT for authentication

### Frontend
- React 18
- Vite
- React Router
- Axios
- Socket.io-client

### DevOps
- Docker & Docker Compose
- Nginx
- GitHub Actions
- PostgreSQL
- Redis

## Getting Started

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.10+ (for local development)

### Quick Start

1. Clone the repository
```bash
git clone <repository-url>
cd talk-to-me-uganda
```

2. Run setup script
```bash
chmod +x setup.sh
./setup.sh
```

3. Start with Docker Compose
```bash
docker-compose up
```

4. Access the application
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000/api
- Nginx: http://localhost

### Local Development

#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python run.py
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Environment Configuration

Copy `.env.example` files to `.env` and update with your configuration:

```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

## Testing

### Backend Tests
```bash
cd backend
pytest tests/ -v
```

### Frontend Linting
```bash
cd frontend
npm run lint
```

## Database Migrations

```bash
cd backend
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

## Deployment

### Using Docker Compose
```bash
docker-compose -f docker-compose.yml up -d
```

### Using GitHub Actions
Push to the main branch to trigger automatic deployment.

## API Documentation

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/verify` - Verify token
- `POST /api/auth/reset-password` - Reset password

### Chat
- `POST /api/chat/message` - Send chat message
- `GET /api/chat/history/:sessionId` - Get chat history
- `POST /api/chat/session` - Start new session

### Assessments
- `GET /api/assessment` - Get available assessments
- `POST /api/assessment` - Submit assessment
- `GET /api/assessment/:id/results` - Get assessment results

### Counselling
- `GET /api/counselling/counsellors` - Get counsellors
- `POST /api/counselling/book` - Book session
- `GET /api/counselling/appointments` - Get appointments

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Support

For crisis support, contact:
- National Crisis Hotline: 0800 XXXX XXXX
- Email: support@talk-to-me.ug

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Uganda Ministry of Health
- Mental health professionals and counsellors
- Community mental health advocates
run