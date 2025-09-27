#!/bin/bash

# ClaimMax AI Backend - Development Setup (No External APIs Required)

echo "🚀 Setting up ClaimMax AI Backend for Development..."

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file for development..."
    cat > .env << EOF
# Database Configuration
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/claimmax_ai
REDIS_URL=redis://localhost:6379/0

# JWT Configuration
SECRET_KEY=dev-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# OpenAI Configuration (OPTIONAL - leave empty for mock responses)
OPENAI_API_KEY=

# AWS Configuration (OPTIONAL - leave empty for local file storage)
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_REGION=us-east-1
S3_BUCKET_NAME=claimmax-ai-files

# Application Configuration
ENVIRONMENT=development
DEBUG=true
CORS_ORIGINS=["http://localhost:3000", "http://127.0.0.1:3000"]

# File Upload Configuration
MAX_FILE_SIZE=10485760
ALLOWED_EXTENSIONS=["jpg", "jpeg", "png", "gif", "pdf"]

# Celery Configuration
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/2
EOF
    echo "✅ .env file created with development settings"
else
    echo "✅ .env file already exists"
fi

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Start services with Docker Compose
echo "🐳 Starting services with Docker Compose..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 15

# Run database migrations
echo "🗄️  Running database migrations..."
docker-compose exec web alembic upgrade head

# Check if services are healthy
echo "🔍 Checking service health..."
if curl -f http://localhost:8000/api/v1/health/ > /dev/null 2>&1; then
    echo ""
    echo "🎉 ClaimMax AI Backend is ready!"
    echo ""
    echo "📚 API Documentation: http://localhost:8000/docs"
    echo "🌸 Celery Flower: http://localhost:5555"
    echo "🗄️  Database: PostgreSQL on localhost:5432"
    echo "📦 Redis: localhost:6379"
    echo ""
    echo "🔧 Features available:"
    echo "  ✅ User authentication"
    echo "  ✅ Claim management"
    echo "  ✅ Local file uploads"
    echo "  ✅ Mock AI responses"
    echo "  ✅ Background job processing"
    echo ""
    echo "🛑 To stop services: docker-compose down"
    echo "📊 To view logs: docker-compose logs -f"
else
    echo "❌ Backend health check failed. Check logs with: docker-compose logs"
fi
