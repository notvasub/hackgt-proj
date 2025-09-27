#!/bin/bash

# ClaimMax AI Backend Startup Script

echo "🚀 Starting ClaimMax AI Backend..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from template..."
    cp env.example .env
    echo "📝 Please edit .env file with your configuration before running again."
    exit 1
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
sleep 10

# Run database migrations
echo "🗄️  Running database migrations..."
docker-compose exec web alembic upgrade head

# Check if services are healthy
echo "🔍 Checking service health..."
if curl -f http://localhost:8000/api/v1/health/ > /dev/null 2>&1; then
    echo "✅ Backend is healthy and ready!"
    echo "📚 API Documentation: http://localhost:8000/docs"
    echo "🌸 Celery Flower: http://localhost:5555"
    echo "🛑 To stop services: docker-compose down"
else
    echo "❌ Backend health check failed. Check logs with: docker-compose logs"
fi
