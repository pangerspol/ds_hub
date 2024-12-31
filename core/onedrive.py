import requests
from msal import PublicClientApplication

class OneDriveManager:
    def __init__(self, client_id, client_secret, tenant_id):
        self.client_id = client_id
        self.client_secret = client_secret
        self.tenant_id = tenant_id
        self.token = None
        self.api_url = "https://graph.microsoft.com/v1.0"

    def authenticate(self):
        app = PublicClientApplication(
            self.client_id,
            authority=f"https://login.microsoftonline.com/{self.tenant_id}"
            )
        result = app.acquire_token_by_username_password(
            username=os.environ.get("MY_USERNAME"),
            password=os.environ.get("MY_PASSWORD"),
            scopes=["Files.ReadWrite", "Sites.ReadWrite.All"]
        )
        self.token = result['access_token']

    def create_folder(self, parent_path, folder_name):
        url = f"{self.api_url}/me/drive/root:/{parent_path}/{folder_name}:/children"
        headers = {"Athorization": f"Bearer {self.token}"}
        data = {"name": folder_name, "folder": {}, "@microsoft.graph.conflictBehavior": "rename"}
        response = requests.post(url, json=data, headers=headers)
        return response.json()