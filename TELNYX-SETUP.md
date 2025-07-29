# Telnyx Webhook Setup Guide

## **Current Issue:**
Your phone number is going directly to Asterisk instead of through Telnyx webhooks to your Flask app.

## **Solution: Configure Telnyx Webhooks**

### **Step 1: Update Telnyx Voice Application**

1. **Go to Telnyx Mission Control:** https://portal.telnyx.com/
2. **Navigate to:** Voice → Applications
3. **Find your application** (the one connected to +1 480 786 8280)
4. **Click "Edit"** on your application

### **Step 2: Configure Webhook URL**

**Set the webhook URL to:**
```
http://147.182.184.153/webhooks/telnyx
```

**Or if you want to test locally first:**
```
http://147.182.184.153:5000/webhooks/telnyx
```

### **Step 3: Configure Call Handling**

**In your Telnyx Voice Application settings:**

1. **Webhook URL:** `http://147.182.184.153/webhooks/telnyx`
2. **Webhook Failover URL:** (leave blank for now)
3. **HTTP Method:** POST
4. **Webhook Timeout:** 10 seconds

### **Step 4: Test the Setup**

1. **Call your number:** +1 480 786 8280
2. **Check Flask logs:** 
   ```bash
   # On your droplet
   docker-compose logs -f flask-app
   ```
3. **Check webhook endpoint:**
   ```bash
   curl http://147.182.184.153/webhooks/telnyx
   ```

## **Expected Flow:**

1. **Call comes in** → **Telnyx receives it**
2. **Telnyx sends webhook** → **Your Flask app**
3. **Flask app answers call** → **Plays greeting**
4. **Call continues** → **Flask handles the rest**

## **Troubleshooting:**

### **If webhook doesn't work:**
1. **Check if Flask is running:**
   ```bash
   docker-compose ps
   ```

2. **Check Flask logs:**
   ```bash
   docker-compose logs flask-app
   ```

3. **Test webhook manually:**
   ```bash
   curl -X POST http://147.182.184.153/webhooks/telnyx \
     -H "Content-Type: application/json" \
     -d '{"test": "data"}'
   ```

### **If you want to keep Asterisk for now:**
You can run both systems and gradually migrate:
- **Asterisk:** Direct call handling (current)
- **Flask:** Webhook-based handling (new)

## **Next Steps:**
1. Update Telnyx webhook URL
2. Deploy Flask app to droplet
3. Test the new flow
4. Gradually migrate from Asterisk to Flask 