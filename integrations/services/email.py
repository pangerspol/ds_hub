import requests
import time
import msal
from django.template.loader import render_to_string
from django.conf import settings
from decouple import config

class EmailService:
    def __init__(self):
        self.client_id = config("CLIENT_ID")
        self.client_secret = config("CLIENT_SECRET")
        self.tenant_id = config("TENANT_ID")
        self.access_token = None
        self.token_expiry = 0  # Unix timestamp when token expires
        self.base_url = "https://graph.microsoft.com/v1.0"

    def authenticate(self):
        """Retrieves a new OAuth2 token if expired, otherwise returns cached token."""
        if self.access_token and time.time() < self.token_expiry:
            print("Already Authenticated")
            return self.access_token  # Return cached token if still valid

        print("Fetching new access token...")
        authority = f"https://login.microsoftonline.com/{self.tenant_id}"
        app = msal.ConfidentialClientApplication(self.client_id, authority=authority, client_credential=self.client_secret)
        token_data = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])

        if "access_token" in token_data:
            self.access_token = token_data["access_token"]
            self.token_expiry = time.time() + int(token_data["expires_in"]) - 60  # Store expiry time (buffer 60s)
            print("Authentication Successful")
            return self.access_token
        else:
            raise Exception(f"Failed to authenticate with Outlook: {token_data.get('error_description', token_data)}")

    def send_email(self, template_name, subject, recipient_list, context, from_email=None, cc_list=None, bcc_list=None, reply_to_message_id=None):
        access_token = self.authenticate()  # Ensure token is valid
        from_email = from_email or settings.DEFAULT_FROM_EMAIL

        # Load and render the email template
        html_content = render_to_string(f"entries/email_templates/{template_name}.html", context)

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        email_data = {
            "message": {
                "subject": subject,
                "body": {
                    "contentType": "HTML",
                    "content": html_content
                },
                "from": {"emailAddress": {"address": from_email}},
                "toRecipients": [{"emailAddress": {"address": email}} for email in recipient_list]
            }
        }

        # Add CC, BCC, and Reply-To if provided
        if cc_list:
            email_data["message"]["ccRecipients"] = [{"emailAddress": {"address": email}} for email in cc_list]
        if bcc_list:
            email_data["message"]["bccRecipients"] = [{"emailAddress": {"address": email}} for email in bcc_list]
        if reply_to_message_id:
            email_data["message"]["replyTo"] = [{"emailAddress": {"address": reply_to_message_id}}]

        response = requests.post(f"{self.base_url}/users/{from_email}/sendMail", headers=headers, json=email_data)


        if response.status_code == 202:
            print(f"Email sent successfully! from {from_email}")
        else:
            raise Exception(f"Failed to send email: {response.text}")


