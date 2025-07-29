#!/bin/bash

# DigitalOcean Droplet Deployment Script for Asterisk Flask App

echo "🚀 Deploying Asterisk Flask App to DigitalOcean Droplet..."

# Update system
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Docker
echo "🐳 Installing Docker..."
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
echo "📦 Installing Docker Compose..."
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Create app directory
echo "📁 Setting up application directory..."
mkdir -p /opt/asterisk-flask
cd /opt/asterisk-flask

# Copy application files (you'll need to upload these)
echo "📋 Application files should be uploaded to /opt/asterisk-flask/"

# Create logs directory
mkdir -p logs

# Set up environment file
echo "🔧 Setting up environment variables..."
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp env.example .env
    echo "⚠️  Please edit .env file with your actual API keys!"
    echo "   nano .env"
fi

# Build and start the application
echo "🔨 Building and starting the application..."
sudo docker-compose up -d --build

# Set up firewall
echo "🔥 Configuring firewall..."
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw --force enable

echo "✅ Deployment complete!"
echo "🌐 Your app should be running on http://$(curl -s ifconfig.me)"
echo "📝 Don't forget to:"
echo "   1. Edit .env file with your API keys"
echo "   2. Update Telnyx webhook URL to your droplet's IP"
echo "   3. Set up a domain name (optional but recommended)" 