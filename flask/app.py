from flask import Flask, request, jsonify
import os
import logging
import json
import requests
from datetime import datetime

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment variables
TELNYX_API_KEY = os.getenv('TELNYX_API_KEY')
GOOGLE_SHEETS_CREDENTIALS = os.getenv('GOOGLE_SHEETS_CREDENTIALS')
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

@app.route('/webhooks/telnyx', methods=['POST', 'GET'])
def handle_telnyx_webhook():
    """Main webhook handler for all Telnyx events"""
    if request.method == 'GET':
        return jsonify({
            'status': 'webhook endpoint ready',
            'message': 'Send POST requests here'
        })
    
    try:
        data = request.get_json()
        logger.info(f"Received event: {data.get('event_type', 'unknown')}")
        logger.info(f"Call data: {json.dumps(data, indent=2)}")
        
        # Handle different event types
        event_type = data.get('event_type')
        
        if event_type == 'call.initiated':
            handle_call_initiated(data)
        elif event_type == 'call.answered':
            handle_call_answered(data)
        elif event_type == 'call.hangup':
            handle_call_hangup(data)
        
        return jsonify({'status': 'success'}), 200
        
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        return jsonify({'error': str(e)}), 500

def handle_call_initiated(data):
    """Handle incoming call initiation"""
    try:
        from_number = data.get('payload', {}).get('from')
        to_number = data.get('payload', {}).get('to')
        logger.info(f"Incoming call from {from_number} to {to_number}")
        
        # Log to Google Sheets
        log_to_sheet(data)
        
        # Answer the call
        call_control_id = data.get('payload', {}).get('call_control_id')
        if call_control_id:
            answer_call(call_control_id)
            
    except Exception as e:
        logger.error(f"Failed to log to sheet: {str(e)}")

def handle_call_answered(data):
    """Handle call answered event"""
    call_control_id = data.get('payload', {}).get('call_control_id')
    logger.info(f"Answered call {call_control_id}")

def handle_call_hangup(data):
    """Handle call hangup event"""
    call_control_id = data.get('payload', {}).get('call_control_id')
    logger.info(f"Call ended: {call_control_id}")

def answer_call(call_control_id):
    """Answer incoming call using Telnyx API"""
    try:
        headers = {
            'Authorization': f'Bearer {TELNYX_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        # Answer the call
        answer_url = f"https://api.telnyx.com/v2/calls/{call_control_id}/actions/answer"
        answer_response = requests.post(answer_url, headers=headers)
        
        if answer_response.status_code == 200:
            logger.info(f"Successfully answered call {call_control_id}")
            
            # Play greeting
            speak_url = f"https://api.telnyx.com/v2/calls/{call_control_id}/actions/speak"
            speak_data = {
                "payload": "Hello, you've reached Anthony Barragan. Please state your name and reason for calling, and I'll get back to you shortly.",
                "voice": "female",
                "language": "en-US"
            }
            
            speak_response = requests.post(speak_url, headers=headers, json=speak_data)
            if speak_response.status_code == 200:
                logger.info(f"Successfully played greeting for call {call_control_id}")
            else:
                logger.error(f"Failed to play greeting: {speak_response.text}")
                
        else:
            logger.error(f"Failed to answer call: {answer_response.text}")
            
    except Exception as e:
        logger.error(f"Error answering call: {str(e)}")

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
    app.run(host='0.0.0.0', port=5000, debug=True)
