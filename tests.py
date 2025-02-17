from django.test import TestCase
from integrations.services.sharepoint import SharePointManager

# Create your tests here.
sharepoint_manager = SharePointManager()

print(sharepoint_manager.get_all_drives_in_site())