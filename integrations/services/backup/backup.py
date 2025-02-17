"""def authenticate(self):
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
            print("Full Error Response", result)
            error_message = result.get("error_description", result.get("error", "Unknown error"))
            raise Exception(f"Authentication failed: {error_message}")"""


def upload_file_to_sharepoint(self, file, folder_id, document_type, custom_name=None):
        self.authenticate()

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/octet-stream"
        }

        if custom_name:
            file_name = f"{custom_name}.pdf"
        else:
            file_name = f"{document_type}.pdf"

        url = f"{self.base_url}/sites/{self.site_id}/drives/{self.open_requests_drive_id}/items/{folder_id}:/{file_name}:/createUploadSession"
        
        response = requests.post(url, headers=headers)
        if response.status_code != 200:
            logging.error(f"Failed to create upload session: {response.text}")
            return None

        upload_url = response.json().get('uploadUrl')

        # Read the file content from InMemoryUploadedFile
        file_data = file.read()

        response = requests.put(upload_url, headers=headers, data=file_data)

        # Upload the file in chunks
        chunk_size = 327680  # 320 KB
        file_size = file.size
        with file.open('rb') as f:
            for chunk_start in range(0, file_size, chunk_size):
                chunk_end = min(chunk_start + chunk_size, file_size) - 1
                chunk_data = f.read(chunk_size)
                chunk_headers = {
                    "Authorization": f"Bearer {self.access_token}",
                    "Content-Range": f"bytes {chunk_start}-{chunk_end}/{file_size}"
                }
                chunk_response = requests.put(upload_url, headers=chunk_headers, data=chunk_data)
                if chunk_response.status_code not in [200, 201, 202]:
                    logging.error(f"Failed to upload chunk: {chunk_response.text}")
                    return None, None

        # Extract SharePoint file URL from the response
        uploaded_file_url = chunk_response.json().get('webUrl')
        uploaded_file_id = chunk_response.json().get('id')
        return uploaded_file_url, uploaded_file_id