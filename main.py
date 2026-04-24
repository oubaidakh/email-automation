import time
import os
import logging
from dotenv import load_dotenv
from storage import Database
from data_source import CSVDataSource
from email_service import EmailService

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

# Load environment variables
load_dotenv()

def run_worker():
    logging.info("Starting Background Worker...")
    
    # Initialize components
    db = Database()
    data_source = CSVDataSource("users.csv")
    email_service = EmailService()
    
    check_interval = int(os.getenv('CHECK_INTERVAL', 30))
    
    while True:
        try:
            logging.info("Checking for new users...")
            new_users = data_source.get_new_users(db)
            
            if not new_users:
                logging.info("No new users detected.")
            else:
                logging.info(f"Detected {len(new_users)} new users.")
                
                for user in new_users:
                    name = user['name']
                    email = user['email']
                    
                    logging.info(f"Processing user: {name} ({email})")
                    
                    # Send email
                    success = email_service.send_welcome_email(name, email)
                    
                    if success:
                        # Mark as processed in DB
                        db.mark_as_processed(email)
                        logging.info(f"Successfully processed {email}")
                    else:
                        logging.error(f"Failed to process {email}. Will retry in next loop.")
                    
                    # Small delay between emails to avoid rate limits
                    time.sleep(1)

        except Exception as e:
            logging.error(f"Unexpected error in worker loop: {e}")
        
        logging.info(f"Sleeping for {check_interval} seconds...")
        time.sleep(check_interval)

if __name__ == "__main__":
    run_worker()
