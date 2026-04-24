import os
import logging
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

class EmailService:
    def __init__(self):
        self.api_key = os.getenv('EMAIL_API_KEY')
        self.sender_email = os.getenv('SENDER_EMAIL')
        self.sender_name = os.getenv('SENDER_NAME', 'Our Community')
        
        if not self.api_key or not self.sender_email:
            logging.error("EMAIL_API_KEY or SENDER_EMAIL environment variables are not set!")

        # Configure Brevo API
        self.configuration = sib_api_v3_sdk.Configuration()
        self.configuration.api_key['api-key'] = self.api_key

    def send_welcome_email(self, name, email):
        """Sends a personalized welcome email using Brevo (Sendinblue)."""
        if not self.api_key or not self.sender_email:
            logging.error("Brevo credentials missing.")
            return False

        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(self.configuration))
        
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
            to=[{"email": email, "name": name}],
            sender={"email": self.sender_email, "name": self.sender_name},
            subject="Welcome to Our Community!",
            html_content=self._get_html_template(name)
        )

        try:
            api_response = api_instance.send_transitional_emails(send_smtp_email)
            logging.info(f"Email sent to {email}. Message ID: {api_response.message_id}")
            return True
        except ApiException as e:
            logging.error(f"Exception when calling Brevo API: {e}")
            return False

    def _get_html_template(self, name):
        """Returns a premium HTML email template."""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 20px auto; padding: 20px; border: 1px solid #e0e0e0; border-radius: 12px; background: #ffffff; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }}
                .header {{ background: linear-gradient(135deg, #6366f1 0%, #a855f7 100%); padding: 30px; border-radius: 8px 8px 0 0; text-align: center; color: white; }}
                .content {{ padding: 30px; }}
                .footer {{ text-align: center; font-size: 12px; color: #777; padding: 20px; }}
                .button {{ display: inline-block; padding: 12px 24px; background: #6366f1; color: white; text-decoration: none; border-radius: 6px; font-weight: bold; margin-top: 20px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Welcome, {name}!</h1>
                </div>
                <div class="content">
                    <p>Hello {name},</p>
                    <p>We're thrilled to have you join us. Your account is now active and ready to go.</p>
                    <p>Stay tuned for exciting updates and community events!</p>
                    <a href="#" class="button">Visit Your Dashboard</a>
                </div>
                <div class="footer">
                    &copy; 2026 Your Organization. All rights reserved.
                </div>
            </div>
        </body>
        </html>
        """
