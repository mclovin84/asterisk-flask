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
        webhook_data = request.get_json()
        logger.info(f"Received webhook data: {json.dumps(webhook_data, indent=2)}")
        
        # Extract event type and payload from the correct structure
        event_type = webhook_data.get('event_type')
        payload = webhook_data.get('payload', {})
        
        logger.info(f"Processing event: {event_type}")
        logger.info(f"Payload: {json.dumps(payload, indent=2)}")
        
        # Handle different event types
        if event_type == 'call.initiated':
            logger.info("Handling call.initiated event")
            return handle_call_initiated(webhook_data)
        elif event_type == 'call.answered':
            logger.info("Handling call.answered event")
            return handle_call_answered(webhook_data)
        elif event_type == 'call.hangup':
            logger.info("Handling call.hangup event")
            return handle_call_hangup(webhook_data)
        else:
            logger.info(f"Unhandled event type: {event_type}")
            return jsonify({'status': 'ignored'}), 200
        
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        return jsonify({'error': str(e)}), 500

def handle_call_initiated(data):
    """Handle incoming call initiation"""
    try:
        payload = data.get('payload', {})
        from_number = payload.get('from')
        to_number = payload.get('to')
        call_control_id = payload.get('call_control_id')
        
        logger.info(f"Incoming call from {from_number} to {to_number}")
        logger.info(f"Call control ID: {call_control_id}")
        
        # Log to Google Sheets
        log_to_sheet(data)
        
        # Answer the call
        if call_control_id:
            logger.info(f"Attempting to answer call {call_control_id}")
            answer_call(call_control_id)
            return jsonify({'status': 'call_answered'}), 200
        else:
            logger.error("No call_control_id found in payload")
            return jsonify({'error': 'No call_control_id'}), 400
            
    except Exception as e:
        logger.error(f"Failed to handle call initiated: {str(e)}")
        return jsonify({'error': str(e)}), 500

def handle_call_answered(data):
    """Handle call answered event"""
    payload = data.get('payload', {})
    call_control_id = payload.get('call_control_id')
    logger.info(f"Call answered: {call_control_id}")
    return jsonify({'status': 'call_answered'}), 200

def handle_call_hangup(data):
    """Handle call hangup event"""
    payload = data.get('payload', {})
    call_control_id = payload.get('call_control_id')
    hangup_cause = payload.get('hangup_cause', 'unknown')
    logger.info(f"Call ended: {call_control_id}, cause: {hangup_cause}")
    return jsonify({'status': 'call_ended'}), 200

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
