#!/bin/bash

# Simple deployment script for Asterisk + Flask
# Usage: ./deploy.sh [droplet-ip]

set -e

DROPLET_IP=${1:-"147.182.184.153"}
SSH_KEY="newSSH"

echo "🚀 Deploying Asterisk + Flask to $DROPLET_IP"

# Check if SSH key exists
if [ ! -f "$SSH_KEY" ]; then
    echo "❌ SSH key $SSH_KEY not found!"
    echo "Please make sure your SSH key is in the current directory"
    exit 1
fi

# Copy files to droplet
echo "📁 Copying files to droplet..."
scp -i $SSH_KEY -r . root@$DROPLET_IP:/opt/asterisk-flask/

# SSH to droplet and deploy
echo "🔧 Deploying on droplet..."
ssh -i $SSH_KEY root@$DROPLET_IP << 'EOF'
    cd /opt/asterisk-flask
    
    # Install Docker if not installed
    if ! command -v docker &> /dev/null; then
        echo "🐳 Installing Docker..."
        curl -fsSL https://get.docker.com -o get-docker.sh
        sh get-docker.sh
        systemctl start docker
        systemctl enable docker
    fi
    
    # Install Docker Compose if not installed
    if ! command -v docker-compose &> /dev/null; then
        echo "📦 Installing Docker Compose..."
        curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
        chmod +x /usr/local/bin/docker-compose
    fi
    
    # Stop any existing containers
    echo "🛑 Stopping existing containers..."
    docker-compose down || true
    
    # Build and start containers
    echo "🔨 Building and starting containers..."
    docker-compose up -d --build
    
    # Wait for services to start
    echo "⏳ Waiting for services to start..."
    sleep 30
    
    # Check status
    echo "📊 Checking service status..."
    docker-compose ps
    docker-compose logs --tail=20
EOF

echo "✅ Deployment complete!"
echo "📞 Test your phone system by calling +1 480 786 8280"
echo "🌐 Flask app should be available at http://$DROPLET_IP:5000" 