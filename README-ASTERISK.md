# Asterisk PBX Setup with Flask Integration

This guide will help you set up Asterisk PBX with SIP trunking to replace Telnyx and create your own phone system.

## Overview

You're moving from Telnyx to a self-hosted Asterisk solution. This gives you:
- **Complete control** over your phone system
- **Lower costs** ($25/month vs $200+/month)
- **No verification hassles** from US-based providers
- **Full customization** for AI calling bots, cold calling, etc.

## Current Status

✅ **Asterisk installed** on Digital Ocean droplet (143.198.146.107)  
✅ **Basic configuration** in place  
❌ **SIP trunk provider** needs to be configured  
❌ **Flask integration** needs to be updated  

## Next Steps

### 1. Choose a SIP Trunk Provider

**Recommended: Infobip (Croatia)**
- Less verification than US providers
- Good pricing
- Support for US numbers
- Go to: https://www.infobip.com/sip-trunking

**Alternative: Local Eastern European Providers**
- Search for "SIP trunking" + "Eastern Europe"
- Many have minimal verification requirements

### 2. Configure Asterisk on Your Server

SSH into your server and run the setup script:

```bash
ssh root@143.198.146.107
cd /root
wget https://raw.githubusercontent.com/your-repo/asterisk-flask/main/setup-asterisk.sh
chmod +x setup-asterisk.sh
./setup-asterisk.sh
```

### 3. Update SIP Trunk Configuration

After getting your SIP trunk provider details, edit `/etc/asterisk/pjsip.conf`:

```bash
nano /etc/asterisk/pjsip.conf
```

Replace these values with your provider's details:
- `YOUR_USERNAME` → Your SIP trunk username
- `YOUR_PASSWORD` → Your SIP trunk password  
- `YOUR_PROVIDER_IP` → Your provider's SIP server IP

### 4. Test the Configuration

```bash
# Reload Asterisk
asterisk -rx "core reload"

# Check endpoints
asterisk -rx "pjsip show endpoints"

# Check dialplan
asterisk -rx "dialplan show"

# Monitor calls
asterisk -rx "core show channels"
```

### 5. Update Flask Application

Replace your current Flask app with the Asterisk version:

```bash
# Stop current Flask app
# Update to use asterisk_app.py instead of app.py
```

### 6. Deploy Updated Flask App

```bash
# Update your Railway deployment
# Change the main file to asterisk_app.py
```

## Configuration Files

### Asterisk Configuration

**`/etc/asterisk/pjsip.conf`** - SIP trunk configuration
**`/etc/asterisk/extensions.conf`** - Call routing logic  
**`/etc/asterisk/manager.conf`** - AMI interface for Flask

### Flask Application

**`flask/asterisk_app.py`** - New Flask app that connects to Asterisk AMI

## Testing Your Setup

### 1. Test Incoming Calls
Call your number (480-786-8280) and you should hear:
- "Hello world"
- Your caller ID number
- "Demo about to try"

### 2. Test Outbound Calls
Use the Flask API:
```bash
curl -X POST http://your-flask-app/call/outbound \
  -H "Content-Type: application/json" \
  -d '{"to": "+1234567890"}'
```

### 3. Monitor Logs
```bash
# On your server
tail -f /var/log/asterisk/full

# Flask app logs
# Check your Railway deployment logs
```

## Cost Comparison

| Service | Monthly Cost | Features |
|---------|-------------|----------|
| Telnyx | $200+ | Full service, lots of verification |
| Asterisk + SIP Trunk | $25-50 | Complete control, minimal verification |
| Savings | $150-175/month | Plus full customization |

## SIP Trunk Provider Options

### Infobip (Recommended)
- **Location**: Croatia
- **Verification**: Minimal
- **US Numbers**: Yes
- **Pricing**: Competitive
- **Setup**: Self-service

### Other International Options
- **MessageBird**: Netherlands (still has US ties)
- **Local Eastern European**: Various providers with minimal verification
- **Search terms**: "SIP trunking Eastern Europe" + "no verification"

## Troubleshooting

### Common Issues

1. **Asterisk not starting**
   ```bash
   systemctl status asterisk
   journalctl -u asterisk -f
   ```

2. **SIP trunk not registering**
   ```bash
   asterisk -rx "pjsip show endpoints"
   asterisk -rx "pjsip show registrations"
   ```

3. **Flask can't connect to Asterisk**
   - Check AMI configuration in `/etc/asterisk/manager.conf`
   - Verify firewall allows port 5038
   - Check credentials in Flask app

4. **No audio on calls**
   - Check codec configuration
   - Verify RTP ports (10000-20000)
   - Check firewall settings

### Debug Commands

```bash
# Asterisk CLI
asterisk -r

# Show all channels
asterisk -rx "core show channels"

# Show SIP registrations
asterisk -rx "pjsip show registrations"

# Show dialplan
asterisk -rx "dialplan show"

# Monitor calls
asterisk -rx "core show channels verbose"
```

## Security Considerations

1. **Firewall Configuration**
   ```bash
   # Allow SIP traffic
   ufw allow 5060/udp
   ufw allow 5061/tcp
   ufw allow 10000:20000/udp  # RTP ports
   ```

2. **AMI Security**
   - Change default password
   - Restrict access to specific IPs
   - Use strong authentication

3. **SIP Security**
   - Use TLS when possible
   - Implement proper authentication
   - Monitor for suspicious activity

## Next Development Steps

Once basic setup is working:

1. **Custom Greetings**
   - Replace default Asterisk prompts
   - Add custom voice prompts

2. **AI Integration**
   - Connect to AI services for voice responses
   - Implement call routing logic

3. **Call Recording**
   - Configure call recording
   - Store recordings securely

4. **Advanced Features**
   - IVR (Interactive Voice Response)
   - Call queuing
   - Voicemail system

## Support

If you encounter issues:

1. Check Asterisk logs: `/var/log/asterisk/full`
2. Check Flask logs: Railway deployment logs
3. Test SIP trunk connectivity
4. Verify firewall settings

## Cost Breakdown

- **Digital Ocean Droplet**: $6/month
- **SIP Trunk Provider**: $15-30/month  
- **Railway Hosting**: $5/month
- **Total**: ~$26-41/month

**Savings**: $159-174/month compared to Telnyx!

---

**Ready to proceed?** Start with step 1 (choosing a SIP trunk provider) and we'll get your Asterisk system up and running! 