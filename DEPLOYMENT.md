# Asterisk + Flask Auto-Deployment Guide

## 🎯 Current Status
- ✅ **Local Cursor workspace** connected to GitHub
- ✅ **Droplet** running at 147.182.184.153
- ✅ **Asterisk** installed and working
- ✅ **Flask app** ready for deployment
- 🔄 **Auto-deployment** needs setup

## 🚀 Auto-Deployment Setup

### Step 1: Set Up GitHub Webhook
1. Go to https://github.com/mclovin84/asterisk-flask/settings/webhooks
2. Click "Add webhook"
3. **Payload URL:** `http://147.182.184.153:9000/hooks/deploy`
4. **Content type:** `application/json`
5. **Events:** Just the `push` event
6. Click "Add webhook"

### Step 2: Configure Droplet Webhook
```bash
# SSH to your droplet
ssh -i newSSH root@147.182.184.153

# Create webhook config
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
cat > /opt/asterisk-flask/deploy.sh << 'EOF'
#!/bin/bash
cd /opt/asterisk-flask
git pull origin main
docker-compose up -d --build
systemctl reload asterisk
echo "Deployment completed at $(date)" >> /opt/asterisk-flask/deploy.log
EOF

chmod +x /opt/asterisk-flask/deploy.sh

# Install and start webhook service
apt install -y webhook
systemctl start webhook
systemctl enable webhook
```

### Step 3: Test Auto-Deployment
1. Make a change in Cursor
2. Commit and push to GitHub
3. Check if deployment triggers automatically

## 🔧 Manual Deployment Commands

### Deploy from Cursor to Droplet:
```bash
# From your local machine
git add .
git commit -m "Update from Cursor"
git push origin main
```

### SSH to Droplet and Deploy:
```bash
ssh -i newSSH root@147.182.184.153
cd /opt/asterisk-flask
git pull origin main
docker-compose up -d --build
```

## 📊 Monitoring

### Check Deployment Status:
```bash
# On droplet
tail -f /opt/asterisk-flask/deploy.log
docker ps
systemctl status asterisk
```

### Check Webhook Logs:
```bash
# On droplet
journalctl -u webhook -f
```

## 🎯 Next Steps
1. Set up auto-deployment
2. Configure environment variables
3. Set up SSL certificates
4. Add monitoring and logging
5. Set up backup system

## 📞 Test Your Setup
Call +1 480 786 8280 to test the current Asterisk setup! 