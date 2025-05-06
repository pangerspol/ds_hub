from msal import ConfidentialClientApplication
import requests, time
from decouple import config
import logging, re
from io import BytesIO

import urllib

class SharePointManager:
    def __init__(self):
        self.client_id = config("CLIENT_ID")
        self.client_secret = config("CLIENT_SECRET")
        self.tenant_id = config("TENANT_ID")
        self.access_token = None
        self.site_id = config("CLOUD_DOCS_SITE_ID")
        self.drive_id = config("CASE_FILES_DRIVE_ID")
        self.open_requests_drive_id = config("OPEN_REQUESTS_DRIVE_ID")
        self.token_expiry = 0  # Unix timestamp when token expires
        self.medical_folder_id = config("MEDICAL_FOLDER_ID")
        self.base_url = "https://graph.microsoft.com/v1.0"
        # logging.basicConfig(level=logging.DEBUG)
    
    def authenticate(self):
        #Retrieves a new OAuth2 token if expired, otherwise returns cached token.
        if self.access_token and time.time() < self.token_expiry:
            #  print("Already Authenticated")
            return self.access_token  # Return cached token if still valid

        url = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token"

        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": "https://graph.microsoft.com/.default"
        }

        response = requests.post(url, data=data)

        if response.status_code == 200:
            token_data = response.json()
            self.access_token = token_data["access_token"]
            self.token_expiry = time.time() + int(token_data["expires_in"]) - 60  # Store expiry time (buffer 60s)
            print("Authentication Successful")
            return self.access_token
        else:
            raise Exception(f"Failed to authenticate with SharePoint: {response.text}")
        
    # Methods -----------------------------------------------------------------------------------------------------------
        
    def list_sites(self):
        self.authenticate()
        
        url = f"{self.base_url}/sites"
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()  # Returns a list of available sites
        else:
            raise Exception(f"Failed to list sites: {response.json()}")

    def get_all_drives_in_site(self):
        self.authenticate()

        url = f"{self.base_url}/sites/{self.site_id}/drives"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json().get('value', [])
        else:
            raise Exception(f"Failed to fetch drives: {response.status_code}, {response.text}")
        
    def get_all_folders_from_drive(self, drive_id=None):
        self.authenticate()

        if not drive_id:
            drive_id = self.open_requests_drive_id
        
        url = f"{self.base_url}/sites/{self.site_id}/drives/{drive_id}/root/children/"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json().get('value', [])
        else:
            raise Exception(f"Failed to fetch folders: {response.status_code}, {response.text}")
    
    def search_folders_by_case_number(self, case_number, folder_names=None):
        self.authenticate()

        url = f"{self.base_url}/sites/{self.site_id}/drives/{self.drive_id}/root/search(q='{case_number}')"
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            raise Exception(f"Failed to search folder: {response.status_code}, {response.text}")

        all_items = response.json().get("value", [])

        # **Step 1: Find the main folder where case_number is at the end**
        main_folder_id = None
        sharepoint_url = None

        for item in all_items:
            if "folder" in item:  # Ensure it's a folder, not a file
                folder_name = item["name"]
                
                # Use `rsplit(" - ", 1)` to split only at the LAST " - "
                parts = re.split(r" - |-", folder_name)  # Splits on " - " or "-"
                
                if len(parts) > 1:  # Ensure there's a case number at the end
                    extracted_case_number = parts[-1]
                    if extracted_case_number == case_number:
                        main_folder_id = item["id"]
                        sharepoint_url = item["webUrl"]
                        break  # Found the main folder, no need to continue

        if not main_folder_id:
            return None if folder_names else (None,)  # Return (None,) if no folders exist

        # **If no subfolder names are requested, return only the main folder ID and sharepoint URL**
        if not folder_names:
            return main_folder_id, sharepoint_url,

        # **Step 2: Look for subfolders inside `main_folder_id`**
        subfolder_url = f"{self.base_url}/sites/{self.site_id}/drives/{self.drive_id}/items/{main_folder_id}/children"

        subfolder_response = requests.get(subfolder_url, headers=headers)

        if subfolder_response.status_code != 200:
            raise Exception(f"Failed to fetch subfolders: {subfolder_response.status_code}, {subfolder_response.text}")

        subfolders = subfolder_response.json().get("value", [])

        # **Find subfolder IDs (Case-Insensitive)**
        folder_names_lower = {name.lower(): name for name in folder_names}  # Mapping of lowercase -> original name
        subfolder_ids = {name: None for name in folder_names}  # Prepare dictionary for storing folder IDs

        for subfolder in subfolders:
            if "folder" in subfolder:
                subfolder_name_lower = subfolder["name"].lower()
                if subfolder_name_lower in folder_names_lower:
                    subfolder_ids[folder_names_lower[subfolder_name_lower]] = subfolder["id"]

        # **Step 3: Create missing subfolders**
        for folder_name in folder_names:
            if subfolder_ids[folder_name] is None:
                logging.info(f"Subfolder '{folder_name}' not found. Creating one...")

                create_folder_url = f"{self.base_url}/sites/{self.site_id}/drives/{self.drive_id}/items/{main_folder_id}/children"
                folder_data = {
                    "name": folder_name,
                    "folder": {},
                    "@microsoft.graph.conflictBehavior": "fail"
                }

                create_response = requests.post(create_folder_url, headers=headers, json=folder_data)

                if create_response.status_code == 201:
                    subfolder_ids[folder_name] = create_response.json().get("id")
                    logging.info(f"Subfolder '{folder_name}' created successfully.")
                else:
                    logging.error(f"Failed to create subfolder '{folder_name}': {create_response.text}")

        return (main_folder_id, sharepoint_url, *[subfolder_ids[name] for name in folder_names])  # Return as separate values
        
    # Folder Management 
    def create_folder(self, provider, invoice_number, client_name, case_number, parent_folder):
        self.authenticate()

        folder_name = f"{provider} - Inv #{invoice_number} - {client_name}_{case_number}"

        url = f"{self.base_url}/sites/{self.site_id}/drives/{self.open_requests_drive_id}/items/root:/{parent_folder}:/children"
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

        payload = {
            "name": folder_name,
            "folder": {},
            "@microsoft.graph.conflictBehavior": "fail" #Avoid duplicates
        }

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 201:
            print(f"Folder '{folder_name}' created successfully.")
            temp_folder_id = response.json().get("id")
            return True, temp_folder_id
        else:
            logging.error(f"Error: {response.status_code} - Failed to create folder {folder_name}: {response.text}")
            return False, None
        
    def delete_folder(self, folder_id):
        self.authenticate()

        url = f"{self.base_url}/sites/{self.site_id}/drives/{self.open_requests_drive_id}/items/{folder_id}"
        
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }

        response = requests.delete(url, headers=headers)

        if response.status_code == 204:
            print(f"Folder deleted successfully.")
            return True
        else:
            logging.error(f"Failed to delete folder: {response.text}")
            return False
    
    def upload_file(self, file, folder_id, document_type, custom_name=None):
        self.authenticate()
        headers = {"Authorization": f"Bearer {self.access_token}"}

        if custom_name:
            file_name = f"{custom_name}.pdf"
        else:
            file_name = f"{document_type}.pdf"

        # Determine file size
        if isinstance(file, BytesIO):
            file_size = file.getbuffer().nbytes
        else:
            file_size = file.size  # Works for Django InMemoryUploadedFile

        # **Small File Upload (≤ 4MB)**
        if file_size <= 4 * 1024 * 1024:  # 4MB limit
            # **Step 1: Create an empty file in SharePoint**
            create_url = f"{self.base_url}/sites/{self.site_id}/drives/{self.open_requests_drive_id}/items/{folder_id}/children"
            create_payload = {
                "@microsoft.graph.conflictBehavior": "replace",
                "name": file_name,
                "file": {}  # Create an empty file
            }

            headers["Content-Type"] = "application/json"
            create_response = requests.post(create_url, headers=headers, json=create_payload)

            if create_response.status_code not in [200, 201]:
                logging.error(f"Failed to create file metadata: {create_response.text}")
                return None, None

            file_id = create_response.json().get("id")

            # **Step 2: Upload File Content**
            upload_url = f"{self.base_url}/sites/{self.site_id}/drives/{self.open_requests_drive_id}/items/{file_id}/content"

            file.seek(0)  # Reset file pointer
            file_data = file.read()

            upload_headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "application/octet-stream",
            }

            upload_response = requests.put(upload_url, headers=upload_headers, data=file_data)

            if upload_response.status_code in [200, 201]:
                return upload_response.json().get('webUrl'), upload_response.json().get('id')
            else:
                logging.error(f"Failed to upload small file: {upload_response.text}")
                return None, None

        # **Chunked Upload for Large Files (> 4MB)**
        else:
            headers["Content-Type"] = "application/json"

            encoded_file_name = urllib.parse.quote(file_name)

            # **Step 1: Create Upload Session**
            url = f"{self.base_url}/sites/{self.site_id}/drives/{self.open_requests_drive_id}/items/{folder_id}:/{encoded_file_name}:/createUploadSession"

            payload = {
                "item": {
                    "@microsoft.graph.conflictBehavior": "replace"
                }
            }

            # logging.debug(f"Creating upload session with URL: {url}")
            # logging.debug(f"Headers: {headers}")
            # logging.debug(f"Payload: {payload}")

            response = requests.post(url, headers=headers, json=payload)

            if response.status_code != 200:
                logging.error(f"Failed to create upload session: {response.text}")
                return None, None

            upload_url = response.json().get('uploadUrl')

            # **Step 2: Upload in Chunks**
            chunk_size = 327680 * 10  # 3.2 MB per chunk (recommended by Microsoft)
            file.seek(0)  # Reset file pointer

            chunk_number = 0
            while True:
                chunk_data = file.read(chunk_size)
                if not chunk_data:
                    break  # Stop when file is fully read

                chunk_start = chunk_number * chunk_size
                chunk_end = chunk_start + len(chunk_data) - 1  # Last byte index

                chunk_headers = {
                    "Authorization": f"Bearer {self.access_token}",
                    "Content-Range": f"bytes {chunk_start}-{chunk_end}/{file_size}",
                    "Content-Length": str(len(chunk_data)),
                    "Content-Type": "application/octet-stream"
                }

                chunk_response = requests.put(upload_url, headers=chunk_headers, data=chunk_data)

                if chunk_response.status_code not in [200, 201, 202]:
                    logging.error(f"Failed to upload chunk {chunk_number}: {chunk_response.text}")
                    return None, None

                chunk_number += 1

            # **Step 3: Extract File Details**
            try:
                uploaded_file_url = chunk_response.json().get('webUrl')
                uploaded_file_id = chunk_response.json().get('id')
                return uploaded_file_url, uploaded_file_id
            except Exception as e:
                logging.error(f"Error parsing final response: {str(e)}")
                return None, None

    # File Download
    def download_file(self, file_id):
        self.authenticate()

        url = f"{self.base_url}/sites/{self.site_id}/drives/{self.open_requests_drive_id}/items/{file_id}/content"
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Accept": "application/json"
        }

        response = requests.get(url, headers=headers, stream=True)

        if response.status_code == 200:
            return BytesIO(response.content)  # Return file content as BytesIO
        else:
            raise Exception(f"Failed to download file: {response.status_code} {response.text}")
        
    def copy_file(self, file_id, target_folder_id, original_drive_id=None, target_drive_id=None, custom_name=None):
        access_token = self.authenticate()  # Ensure token is valid

        original_drive_id = original_drive_id or self.open_requests_drive_id
        target_drive_id = target_drive_id or self.drive_id
        
        if not custom_name:
            get_name_url = f"{self.base_url}/drives/{original_drive_id}/items/{file_id}"
            get_name_headers = {"Authorization": f"Bearer {access_token}"}

            response = requests.get(get_name_url, headers=get_name_headers)

            if response.status_code == 200:
                file_name = response.json().get("name")
            else:
                raise Exception(f"Failed to retrieve file name: {response.text}")
            
        else:
            file_name = custom_name

        access_token = self.authenticate()  # Ensure token is valid
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        copy_url = f"{self.base_url}/drives/{original_drive_id}/items/{file_id}/copy"

        # Destination configuration
        copy_payload = {
            "parentReference": {
                "driveId": target_drive_id,  # Target Drive
                "id": target_folder_id  # Target Folder
            },
            "name": file_name  # Rename file if needed
        }

        response = requests.post(copy_url, headers=headers, json=copy_payload)

        if response.status_code == 202:
            print("File copy operation started successfully!")
            return response
        else:
            raise Exception(f"Failed to copy file: {response.text}")

    