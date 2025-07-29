#!/bin/bash

# Auto-Deployment Setup Script for Asterisk Flask
# Run this on your droplet after SSH'ing in

echo "🚀 Setting up auto-deployment for Asterisk Flask..."

# Install webhook if not already installed
if ! command -v webhook &> /dev/null; then
    echo "📦 Installing webhook..."
    apt update
    apt install -y webhook
fi

# Create webhook configuration
echo "🔧 Creating webhook configuration..."
cat > /etc/webhook.conf << 'EOF'
[
  {
    "id": "deploy",
    "execute-command": "/opt/asterisk-flask/deploy.sh",
    "command-working-directory": "/opt/asterisk-flask"
  }
]
EOF

# Create deploy script
echo "📝 Creating deploy script..."
cat > /opt/asterisk-flask/deploy.sh << 'EOF'
#!/bin/bash
cd /opt/asterisk-flask
echo "Starting deployment at $(date)" >> /opt/asterisk-flask/deploy.log
git pull origin main
if command -v docker-compose &> /dev/null; then
    docker-compose up -d --build
fi
if systemctl is-active --quiet asterisk; then
    systemctl reload asterisk
fi
echo "Deployment completed at $(date)" >> /opt/asterisk-flask/deploy.log
EOF

chmod +x /opt/asterisk-flask/deploy.sh

# Start webhook service
echo "🔄 Starting webhook service..."
systemctl start webhook
systemctl enable webhook

# Check webhook status
echo "📊 Checking webhook status..."
systemctl status webhook

# Test webhook endpoint
echo "🧪 Testing webhook endpoint..."
curl -X POST http://localhost:9000/hooks/deploy

echo "✅ Auto-deployment setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Go to https://github.com/mclovin84/asterisk-flask/settings/webhooks"
echo "2. Click 'Add webhook'"
echo "3. Set Payload URL to: http://147.182.184.153:9000/hooks/deploy"
echo "4. Set Content type to: application/json"
echo "5. Select 'Just the push event'"
echo "6. Click 'Add webhook'"
echo ""
echo "🎯 Test it by making a change in Cursor and pushing to GitHub!" 