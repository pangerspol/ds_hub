import os
import django
from integrations.services.sharepoint import SharePointManager
from integrations.services.email import EmailService
from integrations.services.google_sheets import GoogleSheetManager
from decouple import config
from datetime import datetime

sharepoint_manager = SharePointManager()
google_sheet_manager = GoogleSheetManager()
# Manually set the Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ds_hub.settings")  
django.setup()  # This ensures Django settings are loaded properly

if True:
    # Create your tests here.
    email_manager = EmailService()

    email_manager.send_email(
        "approval_request", 
        "Testing Approval Request", 
        ["paulo@dresslerlaw.com"], 
        {
            "attorney_name": "Mathew Murdock", 
            "client_name": "Karen Page"
        }, 
        None, 
        ["pangerspol@gmail.com"],
        None,
        None
    )
    """file_id = "01VEABP3IG6RN7S5VTABD3TAIQZK7IDKX5"
    target_folder_id = "01VEABP3POZX2F5L5UOJHKY237SW6QI4VX"
    sharepoint_manager.copy_file(file_id, target_folder_id)"""

if False:
    data_list = [
        "219494",                       #"Case ID"
        "Jahdane Walker",               #"Client Name"
        "MRO",                          #"Provider"
        "THNE St Fra",                  #"Facility" 
        "91317597",                     #"Invoice" 
        "24",                           #"Quantity" 
        "FALSE",                        #"isCD"
        "15.76",                        #"Cost" 
        "gabriel@dresslerlaw.com",      #"Requester" 
        "carol@dresslerlaw.com",        #"Paralegal"
        "Hartford",                     #"Office"
        "2025-02-19",                   #"Date Paid"
    ]

    sheet_id = config("GOOGLE_SHEET_MR_PA_ID")
    worksheet_name = datetime.today().strftime("%B")
    google_sheet_manager.log_payment(data_list, sheet_id, "2025")
    google_sheet_manager.log_payment(data_list, sheet_id, worksheet_name)