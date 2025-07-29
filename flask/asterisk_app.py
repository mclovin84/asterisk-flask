from flask import Flask, request, jsonify
import os
import logging
import json
import requests
from datetime import datetime
import socket
import threading
import time

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment variables
ASTERISK_HOST = os.getenv('ASTERISK_HOST', '143.198.146.107')
ASTERISK_PORT = int(os.getenv('ASTERISK_PORT', '5038'))
ASTERISK_USERNAME = os.getenv('ASTERISK_USERNAME', 'admin')
ASTERISK_PASSWORD = os.getenv('ASTERISK_PASSWORD', 'password')
GOOGLE_SHEETS_CREDENTIALS = os.getenv('GOOGLE_SHEETS_CREDENTIALS')
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')

class AsteriskManager:
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.socket = None
        self.connected = False
        
    def connect(self):
        """Connect to Asterisk Manager Interface"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            
            # Login
            login_msg = f"Action: Login\r\nUsername: {self.username}\r\nSecret: {self.password}\r\n\r\n"
            self.socket.send(login_msg.encode())
            
            response = self.socket.recv(1024).decode()
            if "Success" in response:
                self.connected = True
                logger.info("Connected to Asterisk Manager Interface")
                return True
            else:
                logger.error(f"Failed to connect to AMI: {response}")
                return False
                
        except Exception as e:
            logger.error(f"Error connecting to AMI: {str(e)}")
            return False
    
    def send_command(self, command):
        """Send command to Asterisk"""
        if not self.connected:
            if not self.connect():
                return None
                
        try:
            self.socket.send(command.encode())
            response = self.socket.recv(4096).decode()
            return response
        except Exception as e:
            logger.error(f"Error sending command: {str(e)}")
            return None
    
    def originate_call(self, channel, context, exten, priority=1, callerid=None):
        """Originate a call"""
        command = f"Action: Originate\r\nChannel: {channel}\r\nContext: {context}\r\nExten: {exten}\r\nPriority: {priority}\r\n"
        if callerid:
            command += f"Callerid: {callerid}\r\n"
        command += "\r\n"
        
        return self.send_command(command)
    
    def get_channel_status(self, channel):
        """Get status of a specific channel"""
        command = f"Action: Status\r\nChannel: {channel}\r\n\r\n"
        return self.send_command(command)

# Initialize Asterisk Manager
ami = AsteriskManager(ASTERISK_HOST, ASTERISK_PORT, ASTERISK_USERNAME, ASTERISK_PASSWORD)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

@app.route('/webhooks/asterisk', methods=['POST', 'GET'])
def handle_asterisk_webhook():
    """Handle webhooks from Asterisk (if configured)"""
    if request.method == 'GET':
        return jsonify({
            'status': 'asterisk webhook endpoint ready',
            'message': 'Send POST requests here'
        })
    
    try:
        webhook_data = request.get_json()
        logger.info(f"Received Asterisk webhook: {json.dumps(webhook_data, indent=2)}")
        
        # Handle different event types
        event_type = webhook_data.get('event_type')
        
        if event_type == 'call.initiated':
            return handle_call_initiated(webhook_data)
        elif event_type == 'call.answered':
            return handle_call_answered(webhook_data)
        elif event_type == 'call.hangup':
            return handle_call_hangup(webhook_data)
        else:
            logger.info(f"Unhandled event type: {event_type}")
            return jsonify({'status': 'ignored'}), 200
        
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/call/outbound', methods=['POST'])
def make_outbound_call():
    """Make an outbound call through Asterisk"""
    try:
        data = request.get_json()
        to_number = data.get('to')
        from_number = data.get('from', '4807868280')
        
        if not to_number:
            return jsonify({'error': 'Missing to number'}), 400
        
        # Format the channel for outbound call
        channel = f"SIP/trunk/{to_number}"
        
        # Originate the call
        result = ami.originate_call(
            channel=channel,
            context='incoming',
            exten='s',
            callerid=f"{from_number}"
        )
        
        if result and "Success" in result:
            logger.info(f"Successfully originated call to {to_number}")
            return jsonify({'status': 'call_originated', 'to': to_number}), 200
        else:
            logger.error(f"Failed to originate call: {result}")
            return jsonify({'error': 'Failed to originate call'}), 500
            
    except Exception as e:
        logger.error(f"Error making outbound call: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/call/status', methods=['GET'])
def get_call_status():
    """Get current call status"""
    try:
        # This would need to be implemented based on your specific needs
        # You might want to query Asterisk for active channels
        return jsonify({'status': 'no_active_calls'}), 200
    except Exception as e:
        logger.error(f"Error getting call status: {str(e)}")
        return jsonify({'error': str(e)}), 500

def handle_call_initiated(data):
    """Handle incoming call initiation"""
    try:
        from_number = data.get('from')
        to_number = data.get('to')
        
        logger.info(f"Incoming call from {from_number} to {to_number}")
        
        # Log to Google Sheets
        log_to_sheet(data)
        
        return jsonify({'status': 'call_initiated'}), 200
            
    except Exception as e:
        logger.error(f"Failed to handle call initiated: {str(e)}")
        return jsonify({'error': str(e)}), 500

def handle_call_answered(data):
    """Handle call answered event"""
    try:
        call_id = data.get('call_id')
        logger.info(f"Call answered: {call_id}")
        return jsonify({'status': 'call_answered'}), 200
    except Exception as e:
        logger.error(f"Failed to handle call answered: {str(e)}")
        return jsonify({'error': str(e)}), 500

def handle_call_hangup(data):
    """Handle call hangup event"""
    try:
        call_id = data.get('call_id')
        hangup_cause = data.get('hangup_cause', 'unknown')
        logger.info(f"Call ended: {call_id}, cause: {hangup_cause}")
        return jsonify({'status': 'call_ended'}), 200
    except Exception as e:
        logger.error(f"Failed to handle call hangup: {str(e)}")
        return jsonify({'error': str(e)}), 500

def log_to_sheet(data):
    """Log call data to Google Sheets"""
    try:
        if not all([GOOGLE_SHEETS_CREDENTIALS, SPREADSHEET_ID]):
            logger.warning("Google Sheets credentials not configured")
            return
            
        # Parse credentials
        credentials = json.loads(GOOGLE_SHEETS_CREDENTIALS)
        
        # Add timestamp
        data['logged_at'] = datetime.now().isoformat()
        
        # Here you would implement Google Sheets API call
        # For now, just log the data
        logger.info(f"Would log to sheet: {json.dumps(data, indent=2)}")
        
    except Exception as e:
        logger.error(f"Error logging to sheet: {str(e)}")

if __name__ == '__main__':
    # Try to connect to Asterisk on startup
    if ami.connect():
        logger.info("Successfully connected to Asterisk AMI")
    else:
        logger.warning("Could not connect to Asterisk AMI - some features may not work")
    
    app.run(host='0.0.0.0', port=5000, debug=True) 