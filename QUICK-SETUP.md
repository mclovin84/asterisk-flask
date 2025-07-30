# 🚀 Quick Setup Guide - Asterisk + Flask

## What This Does:
- **Asterisk** (Phone system) running in Docker
- **Flask** (Web app) running in Docker  
- **Everything** deployed with one command
- **No more Ubuntu setup** - just Docker containers

## 🎯 One-Command Deployment

### Step 1: Set up your environment
```bash
# Copy the example environment file
cp env.example .env

# Edit with your actual API keys
nano .env
```

### Step 2: Deploy everything
```bash
# Make the deploy script executable
chmod +x deploy.sh

# Deploy to your droplet (replace with your IP)
./deploy.sh 147.182.184.153
```

That's it! Your entire phone system will be running.

## 📞 Test Your Setup
- **Call:** +1 480 786 8280
- **Web App:** http://147.182.184.153:5000
- **Health Check:** http://147.182.184.153:5000/health

## 🔧 What's Included:
- ✅ **Asterisk** (Phone system)
- ✅ **Flask** (Web application) 
- ✅ **Telnyx Integration** (Phone service)
- ✅ **Google Sheets Logging** (Call tracking)
- ✅ **Docker** (Everything containerized)
- ✅ **Auto-restart** (Keeps running)

## 🛠️ Troubleshooting

### Check if everything is running:
```bash
ssh -i newSSH root@147.182.184.153
cd /opt/asterisk-flask
docker-compose ps
```

### View logs:
```bash
docker-compose logs -f
```

### Restart everything:
```bash
docker-compose restart
```

## 🎯 Next Steps (After Basic Setup Works):
1. **ElevenLabs Integration** (AI voices)
2. **OpenRouter Integration** (AI responses)
3. **Custom Call Flows**
4. **Advanced Features**

## 💡 Pro Tips:
- Everything is now in Docker containers
- Easy to move between servers
- Easy to backup and restore
- Easy to scale up

**No more Ubuntu setup headaches!** 🎉 