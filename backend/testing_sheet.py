import gspread
from google.oauth2.service_account import Credentials

# Path to your credentials file
CREDENTIALS_FILE = "integrations/google_sheets_credentials.json"  # Adjust this path if necessary

# Define the required scopes
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

try:
    # Load credentials
    creds = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
    client = gspread.authorize(creds)

    # Open your Google Sheet by its ID
    SHEET_ID = "19lJDnNNIsFNMuqPKyv5R02di1atGW-8azub4tK8ah4s"  # Replace with your actual Sheet ID
    sheet = client.open_by_key(SHEET_ID)

    # Print the sheet title to confirm access
    print(f"✅ Successfully connected to: {sheet.title}")

except Exception as e:
    print(f"❌ Failed to connect: {str(e)}")