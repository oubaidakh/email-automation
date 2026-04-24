from flask import Flask, request, jsonify
import os
import logging
from storage import Database
from email_service import EmailService

app = Flask(__name__)

# Configure Logging
logging.basicConfig(level=logging.INFO)

db = Database()
email_service = EmailService()

@app.route('/new-user', methods=['POST'])
def handle_new_user():
    """
    Endpoint to trigger an email instantly.
    JSON Payload: {"name": "John Doe", "email": "john@example.com"}
    """
    data = request.get_json()
    
    if not data or 'email' not in data:
        return jsonify({"error": "Missing 'email' in request body"}), 400
    
    name = data.get('name', 'Valued User')
    email = data['email'].strip().lower()
    
    # Check if already processed
    if db.is_processed(email):
        return jsonify({"message": "User already processed"}), 200
    
    # Send email
    success = email_service.send_welcome_email(name, email)
    
    if success:
        db.mark_as_processed(email)
        return jsonify({"message": f"Welcome email sent to {email}"}), 200
    else:
        return jsonify({"error": "Failed to send email"}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
