#!/bin/bash

# Deploy Flask App Script
echo "🚀 Deploying Flask app..."

# Check if we're in the right directory
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ Error: docker-compose.yml not found. Run this from the project root."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp env.example .env
    echo "⚠️  Please edit .env file with your actual API keys!"
    echo "   nano .env"
fi

# Install Docker if not installed
if ! command -v docker &> /dev/null; then
    echo "🐳 Installing Docker..."
    apt update
    apt install -y docker.io docker-compose
    systemctl start docker
    systemctl enable docker
fi

# Build and start the Flask app
echo "🔨 Building and starting Flask app..."
docker-compose up -d --build

# Check if containers are running
echo "📊 Checking container status..."
docker-compose ps

# Test the webhook endpoint
echo "🧪 Testing webhook endpoint..."
sleep 5
curl -X GET http://localhost/webhooks/telnyx

echo "✅ Flask app deployment complete!"
echo ""
echo "📋 Next steps:"
echo "1. Edit .env file with your Telnyx API key"
echo "2. Update Telnyx webhook URL to: http://147.182.184.153/webhooks/telnyx"
echo "3. Test by calling +1 480 786 8280"
echo ""
echo "🔧 Useful commands:"
echo "  View logs: docker-compose logs -f flask-app"
echo "  Restart: docker-compose restart flask-app"
echo "  Stop: docker-compose down" 