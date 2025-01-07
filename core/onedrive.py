from msal import ConfidentialClientApplication
import requests
from decouple import config

class OneDriveManager:
    def __init__(self):
        self.client_id = config("CLIENT_ID")
        self.client_secret = config("CLIENT_SECRET")
        self.tenant_id = config("TENANT_ID")
        self.access_token = None

    def authenticate(self):
        app = ConfidentialClientApplication(
            client_id=self.client_id,
            client_credential=self.client_secret,
            authority=f"https://login.microsoftonline.com/{self.tenant_id}"
        )
        result = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
        
        if "access_token" in result:
            self.access_token = result["access_token"]
            print("Authentication successful!")
            return self.access_token
        else:
            raise Exception(f"Authentication failed: {result}")
    
    def create_folder(self, folder_name):
        if not self.access_token:
            raise Exception("Authentication required")
        
        url = "https://graph.microsoft.com/v1.0/me/drive/root/children"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        data = {
            "name": folder_name,
            "folder": {},
            "@microsoft.graph.conflictBehavior": "rename"
        }
        response = requests.post(url, headers=headers, json=data)
        return response.json()
    
    def list_drives(self):
        if not self.access_token:
            raise Exception("Authentication required")
        
        url = "https://graph.microsoft.com/v1.0/drives"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(url, headers=headers)
        return response.json()

    def list_drive_contents(self, drive_id):
        url = f"https://graph.microsoft.com/v1.0/drives/{drive_id}/root/children"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()  # Returns the contents of the drive
        else:
            raise Exception(f"Failed to list drive contents: {response.json()}")
    