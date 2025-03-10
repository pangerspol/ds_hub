import gspread
import logging
from google.oauth2.service_account import Credentials
from datetime import datetime

logger = logging.getLogger(__name__)

class GoogleSheetManager:
    def __init__(self):
        credentials_file="integrations/google_sheets_credentials.json"

        self.scope = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        self.creds = Credentials.from_service_account_file(credentials_file, scopes=self.scope)
        self.client = gspread.authorize(self.creds)

    def get_or_create_worksheet(self, sheet, worksheet_name):
        try:
            worksheet = sheet.worksheet(worksheet_name)  # Get tab if it exists

        except gspread.exceptions.WorksheetNotFound:
            logger.info(f"Tab '{worksheet_name}' not found. Creating new tab...")

            # Create new tab
            worksheet = sheet.add_worksheet(title=worksheet_name, rows="2", cols="12")

            # Define default headers
            default_headers = ["Case ID", "Client Name", "Provider", "Facility", "Invoice", "Quantity", "isCD", "Cost", "Requester", "Paralegal", "Office", "Date Paid"]

            # Insert headers
            worksheet.append_row(default_headers)

            # Apply basic formatting
            self.apply_formatting(worksheet, default_headers)

            logger.info(f"Headers and formatting applied to new tab '{worksheet_name}'.")

        return worksheet
    
    def apply_formatting(self, worksheet, headers):
        try:
            # Freeze the first row (keeps headers visible)
            worksheet.freeze(rows=1)

            # Define header range (A1:F1 based on headers length)
            header_range = f"A1:{chr(64 + len(headers))}1"

            # Apply formatting to headers
            worksheet.format(header_range, {
                "textFormat": {
                    "bold": True,
                    "fontSize": 9,
                    "foregroundColorStyle": {"rgbColor": {"red": 1, "green": 1, "blue": 1}}  # White text
                },
                "backgroundColorStyle": {"rgbColor": {"red": 0.22, "green": 0.36, "blue": 0.53}},  # Light Navy Blue
                "horizontalAlignment": "CENTER",
                "verticalAlignment": "MIDDLE"
            })

            logger.info("Header formatting applied successfully.")
        except Exception as e:
            logger.error(f"Failed to apply formatting: {e}")

    def log_payment(self, data_list, sheet_id, worksheet_name):
        try:
            # Open the Google Sheet
            sheet = self.client.open_by_key(sheet_id)

            # Get or create the tab (worksheet)
            worksheet = self.get_or_create_worksheet(sheet, worksheet_name)

            # Get current data in the sheet
            existing_data = worksheet.get_all_values()

            # Determine where to insert:
            if len(existing_data) == 1:  # Only header exists
                insert_index = 2  # First entry goes directly below the header
            else:
                insert_index = 2  # All other entries go at the top (pushing older rows down)

            # Insert new row at the determined index
            worksheet.insert_row(data_list, index=insert_index)

            # Determine the cell range for formatting (e.g., "A2:F2" for 6 columns)
            col_letter = chr(64 + len(data_list))  # Converts column count to letter (A-F)
            row_range = f"A{insert_index}:{col_letter}{insert_index}"

            # Apply center alignment
            worksheet.format(row_range, {
                "horizontalAlignment": "CENTER",
                "verticalAlignment": "MIDDLE",
                "textFormat": {
                    "bold": False
                }
            })

            logger.info(f"Data logged and formatted in {sheet_id} -> {worksheet_name}: {data_list}")
            return f"Data logged and formatted successfully in {sheet_id} -> {worksheet_name}"
        
        except Exception as e:
            logger.error(f"Failed to log data: {e}")
            raise

