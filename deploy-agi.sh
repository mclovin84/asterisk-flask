#!/bin/bash

echo "🚀 Deploying AGI script to Asterisk..."

# Copy AGI script to Asterisk directory
sudo cp flask-proxy.agi /usr/share/asterisk/agi-bin/

# Make it executable
sudo chmod +x /usr/share/asterisk/agi-bin/flask-proxy.agi

# Install requests if not available
sudo apt-get update
sudo apt-get install -y python3-requests

echo "✅ AGI script deployed successfully!"
echo "📁 Location: /usr/share/asterisk/agi-bin/flask-proxy.agi" 