import pandas as pd
import os
import logging

class CSVDataSource:
    def __init__(self, file_path="users.csv"):
        self.file_path = file_path

    def get_new_users(self, database):
        """
        Reads the CSV and returns a list of users that haven't been processed yet.
        Expected CSV structure: Name, Email
        """
        if not os.path.exists(self.file_path):
            logging.warning(f"File {self.file_path} not found. Creating empty example.")
            self._create_example_file()
            return []

        try:
            # Read CSV
            df = pd.read_csv(self.file_path)
            
            # Basic validation
            if 'Email' not in df.columns:
                logging.error("CSV must have an 'Email' column.")
                return []

            new_users = []
            for _, row in df.iterrows():
                email = str(row['Email']).strip().lower()
                name = str(row.get('Name', 'Valued User')).strip()

                if not database.is_processed(email):
                    new_users.append({
                        'name': name,
                        'email': email
                    })
            
            return new_users

        except Exception as e:
            logging.error(f"Error reading CSV: {e}")
            return []

    def _create_example_file(self):
        """Creates an example users.csv if it doesn't exist."""
        df = pd.DataFrame([
            {'Name': 'John Doe', 'Email': 'john@example.com'},
            {'Name': 'Jane Smith', 'Email': 'jane@example.com'}
        ])
        df.to_csv(self.file_path, index=False)
        logging.info(f"Created example file: {self.file_path}")
