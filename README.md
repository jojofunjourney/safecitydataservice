# safecitywalkdataservice
(ETL) Data pipeline for safe city walk data

## Setup

1. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

2. Create a `.env` file in the project root and add your environment variables:
   ```
   SOCRATA_APP_TOKEN=your_socrata_app_token_here
   GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/google-credentials.json
   ```

3. Obtain a Google Cloud service account key:
   - Go to the Google Cloud Console (https://console.cloud.google.com/)
   - Create a new project or select an existing one
   - Enable the Firestore API for your project
   - Go to "IAM & Admin" > "Service Accounts"
   - Create a new service account or select an existing one
   - Generate a new JSON key and download it
   - Place the JSON key file in a secure location on your machine
   - Update the GOOGLE_APPLICATION_CREDENTIALS path in your .env file to point to this JSON key file

3. Run the script:
   ```
   python crime_data_fetcher.py
   ```
