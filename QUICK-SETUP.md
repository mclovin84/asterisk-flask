# 🚀 Quick Setup Guide

## **Your Current Status:**
- ✅ **Cursor workspace** connected to GitHub
- ✅ **Code pushed** to GitHub repository
- ✅ **Droplet** running at 147.182.184.153
- ✅ **Asterisk** installed and working
- 🔄 **Auto-deployment** ready to set up

## **Step 1: SSH to Your Droplet**
```bash
ssh -i newSSH root@147.182.184.153
```

## **Step 2: Clone Your Repository**
```bash
cd /opt
git clone https://github.com/mclovin84/asterisk-flask.git
cd asterisk-flask
```

## **Step 3: Run Auto-Deployment Setup**
```bash
# Make the script executable
chmod +x setup-auto-deploy.sh

# Run the setup script
./setup-auto-deploy.sh
```

## **Step 4: Set Up GitHub Webhook**
1. **Go to:** https://github.com/mclovin84/asterisk-flask/settings/webhooks
2. **Click:** "Add webhook"
3. **Payload URL:** `http://147.182.184.153:9000/hooks/deploy`
4. **Content type:** `application/json`
5. **Events:** Just the `push` event
6. **Click:** "Add webhook"

## **Step 5: Test Auto-Deployment**
1. **Make a change** in Cursor (like adding a comment to README.md)
2. **Commit and push:**
   ```bash
   git add .
   git commit -m "Test auto-deployment"
   git push origin main
   ```
3. **Check deployment logs:**
   ```bash
   # On your droplet
   tail -f /opt/asterisk-flask/deploy.log
   ```

## **🎯 You're Done!**

Now every time you:
1. **Edit code in Cursor**
2. **Commit and push to GitHub**
3. **Your droplet automatically deploys the changes!**

## **📞 Test Your Phone System**
Call **+1 480 786 8280** to test your Asterisk setup!

## **🔧 Useful Commands**

### Check deployment status:
```bash
# On droplet
tail -f /opt/asterisk-flask/deploy.log
docker ps
systemctl status asterisk
```

### Manual deployment:
```bash
# On droplet
cd /opt/asterisk-flask
git pull origin main
docker-compose up -d --build
```

### Check webhook logs:
```bash
# On droplet
journalctl -u webhook -f
```

## **🎉 Congratulations!**
You now have a fully automated deployment system:
- **Edit in Cursor** → **Push to GitHub** → **Auto-deploy to droplet** → **Phone system updated!** 