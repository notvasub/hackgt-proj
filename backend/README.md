# ClaimMax AI Backend

AI-powered Insurance Claim Optimizer backend built with FastAPI, PostgreSQL, and OpenAI.

## Features

- **User Authentication**: JWT-based authentication with user registration and login
- **Claim Management**: Create, read, update, and delete insurance claims
- **File Upload**: Secure file upload to AWS S3 with image processing
- **AI Processing**: OpenAI-powered claim analysis and optimization
- **Background Jobs**: Celery-based asynchronous processing
- **Database**: PostgreSQL with SQLAlchemy ORM and Alembic migrations
- **API Documentation**: Auto-generated OpenAPI/Swagger documentation
- **Testing**: Comprehensive test suite with pytest
- **Docker**: Full containerization with Docker Compose

## Tech Stack

- **Framework**: FastAPI 0.110+
- **Database**: PostgreSQL 15 with SQLAlchemy 2.0
- **Authentication**: JWT with python-jose
- **File Storage**: AWS S3
- **AI**: OpenAI GPT-4 Vision
- **Background Jobs**: Celery with Redis
- **Testing**: pytest with async support
- **Containerization**: Docker & Docker Compose

## Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Docker & Docker Compose (optional)

### Environment Setup

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd backend
   ```

2. **Create environment file**

   ```bash
   cp env.example .env
   ```

3. **Configure environment variables**
   Edit `.env` with your settings:

   ```env
   # Database
   DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/claimmax_ai

   # OpenAI (OPTIONAL - leave empty for mock responses)
   OPENAI_API_KEY=your-openai-api-key-here

   # AWS (OPTIONAL - leave empty for local file storage)
   AWS_ACCESS_KEY_ID=your-aws-access-key
   AWS_SECRET_ACCESS_KEY=your-aws-secret-key
   S3_BUCKET_NAME=your-s3-bucket

   # JWT
   SECRET_KEY=your-super-secret-key
   ```

### **Quick Start (No External APIs Required)**

For development and testing, you can run the backend without any external API keys:

1. **Minimal configuration** - just set these in `.env`:

   ```env
   DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/claimmax_ai
   SECRET_KEY=your-super-secret-key
   ENVIRONMENT=development
   ```

2. **Start the application**:
   ```bash
   ./start.sh
   ```

The backend will work with:

- ✅ **Local file storage** (no AWS required)
- ✅ **Mock AI responses** (no OpenAI required)
- ✅ **Full API functionality**
- ✅ **Database operations**
- ✅ **Authentication**

### Development Setup

1. **Install dependencies**

   ```bash
   make install
   ```

2. **Start services with Docker**

   ```bash
   make docker-up
   ```

3. **Run database migrations**

   ```bash
   make migrate
   ```

4. **Start development server**
   ```bash
   make start-dev
   ```

The API will be available at `http://localhost:8000`

### Manual Setup (without Docker)

1. **Install dependencies**

   ```bash
   pip install -e .
   ```

2. **Start PostgreSQL and Redis**

   ```bash
   # Start PostgreSQL
   sudo systemctl start postgresql

   # Start Redis
   sudo systemctl start redis
   ```

3. **Run migrations**

   ```bash
   alembic upgrade head
   ```

4. **Start the application**

   ```bash
   uvicorn app.main:app --reload
   ```

5. **Start Celery worker** (in another terminal)
   ```bash
   celery -A app.celery_app worker --loglevel=info
   ```

## API Documentation

Once the server is running, visit:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## API Endpoints

### Authentication

- `POST /api/v1/auth/register` - Register a new user
- `POST /api/v1/auth/login` - Login user

### Claims

- `GET /api/v1/claims/` - List user's claims (paginated)
- `POST /api/v1/claims/` - Create a new claim
- `GET /api/v1/claims/{claim_id}` - Get specific claim
- `PUT /api/v1/claims/{claim_id}` - Update claim
- `DELETE /api/v1/claims/{claim_id}` - Delete claim
- `POST /api/v1/claims/{claim_id}/process` - Start AI processing
- `POST /api/v1/claims/{claim_id}/files` - Upload file to claim
- `GET /api/v1/claims/{claim_id}/files` - Get claim files
- `DELETE /api/v1/claims/files/{file_id}` - Delete file

### Health

- `GET /api/v1/health/` - Basic health check
- `GET /api/v1/health/db` - Database health check

## Database Schema

### Users

- `id` (UUID, Primary Key)
- `email` (String, Unique)
- `hashed_password` (String)
- `full_name` (String, Optional)
- `is_active` (Boolean)
- `is_verified` (Boolean)
- `created_at` (DateTime)
- `updated_at` (DateTime)

### Claims

- `id` (UUID, Primary Key)
- `user_id` (UUID, Foreign Key)
- `incident_description` (Text)
- `incident_date` (DateTime, Optional)
- `incident_location` (String, Optional)
- `insurance_provider` (String)
- `policy_number` (String)
- `claim_type` (Enum: auto, home, health, renters, other)
- `optimized_description` (Text, Optional)
- `damage_assessment` (Text, Optional)
- `claim_justification` (Text, Optional)
- `requested_amount` (Float, Optional)
- `strength_score` (Integer, Optional)
- `status` (Enum: draft, processing, completed, failed)
- `created_at` (DateTime)
- `updated_at` (DateTime)

### Claim Files

- `id` (UUID, Primary Key)
- `claim_id` (UUID, Foreign Key)
- `filename` (String)
- `original_filename` (String)
- `file_size` (Integer)
- `content_type` (String)
- `s3_key` (String)
- `s3_url` (String, Optional)
- `created_at` (DateTime)

### Claim Processing Jobs

- `id` (UUID, Primary Key)
- `claim_id` (UUID, Foreign Key)
- `celery_task_id` (String, Optional)
- `status` (Enum: pending, processing, completed, failed)
- `error_message` (Text, Optional)
- `created_at` (DateTime)
- `started_at` (DateTime, Optional)
- `completed_at` (DateTime, Optional)

## Development

### Running Tests

```bash
make test
```

### Database Migrations

```bash
# Create a new migration
make migrate-create

# Apply migrations
make migrate
```

### Code Quality

```bash
# Format code
black .

# Lint code
ruff check .

# Type checking
mypy .
```

### Docker Commands

```bash
# Start all services
make docker-up

# Stop all services
make docker-down

# View logs
make docker-logs

# Open shell in container
make shell

# Open database shell
make db-shell
```

## Deployment

### Production Environment Variables

```env
ENVIRONMENT=production
DEBUG=false
SECRET_KEY=your-production-secret-key
DATABASE_URL=postgresql+asyncpg://user:pass@prod-db:5432/claimmax_ai
OPENAI_API_KEY=your-openai-key
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
S3_BUCKET_NAME=your-prod-bucket
```

### Docker Production

```bash
# Build production image
docker build -t claimmax-ai-backend .

# Run with production settings
docker run -d \
  --name claimmax-ai-backend \
  -p 8000:8000 \
  -e ENVIRONMENT=production \
  -e DATABASE_URL=your-prod-db-url \
  claimmax-ai-backend
```

## Monitoring

### Celery Flower

Access Celery monitoring at `http://localhost:5555` when running with Docker.

### Health Checks

- Basic: `GET /api/v1/health/`
- Database: `GET /api/v1/health/db`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the MIT License.
