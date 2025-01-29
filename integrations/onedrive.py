from msal import ConfidentialClientApplication
import requests
from decouple import config
import logging

class OneDriveManager:
    def __init__(self):
        self.client_id = config("CLIENT_ID")
        self.client_secret = config("CLIENT_SECRET")
        self.tenant_id = config("TENANT_ID")
        self.access_token = None
        self.site_id = config("CLOUD_DOCS_SITE_ID")
        self.drive_id = config("CASE_FILES_DRIVE_ID")

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
            error_message = result.get("error_description", result)
            raise Exception(f"Authentication failed: {error_message}")
        
    ''' Methods '''
        
    def list_sites(self):
        if not self.access_token:
            raise Exception("Authentication required")
        
        url = "https://graph.microsoft.com/v1.0/sites"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()  # Returns a list of available sites
        else:
            raise Exception(f"Failed to list sites: {response.json()}")

    def get_all_drives_in_site(self):
        """
        Fetch all drives (document libraries) in a given SharePoint site.

        Args:
            access_token (str): Microsoft Graph API access token.
            site_id (str): The SharePoint site ID.

        Returns:
            list: A list of all drives in the site.
        """
        url = f"https://graph.microsoft.com/v1.0/sites/{self.site_id}/drives"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json().get('value', [])
        else:
            raise Exception(f"Failed to fetch drives: {response.status_code}, {response.text}")
    
    def search_folders_by_case_number(self, case_number):
        """
        Search for all folders containing the given case number in their names.

        Args:
            case_number (str): The case number to search for.
            access_token (str): Microsoft Graph API access token.
            site_id (str): The SharePoint site ID.
            drive_id (str): The ID of the document library (Drive).

        Returns:
            list: A list of all matching folder details from SharePoint.
        """
        url = f"https://graph.microsoft.com/v1.0/sites/{self.site_id}/drives/{self.drive_id}/root/search(q='{case_number}')"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            # Return all items in the response
            return data.get('value', [])
        else:
            raise Exception(f"Failed to search folder: {response.status_code}, {response.text}")
        

    