#!/bin/bash

echo "🚀 Deploying updated Asterisk configuration..."

# Copy the updated extensions.conf to the droplet
scp -i ~/.ssh/newSSH asterisk-config/extensions.conf root@147.182.184.153:/etc/asterisk/extensions.conf

# SSH into the droplet and reload Asterisk
ssh -i ~/.ssh/newSSH root@147.182.184.153 << 'EOF'
echo "📞 Reloading Asterisk dialplan..."
asterisk -rx "dialplan reload"

echo "🔍 Checking if from-telnyx context is loaded..."
asterisk -rx "dialplan show from-telnyx"

echo "✅ Configuration deployed!"
echo "📞 Test your call now: +1 480 786 8280"
EOF 