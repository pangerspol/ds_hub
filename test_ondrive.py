from integrations.onedrive import OneDriveManager
from decouple import config
import logging

manager = OneDriveManager()
manager.authenticate()

# Create a folder
#result = manager.create_folder("Test Folder")
#print("Folder creation result:", result)

# List drives available
'''drives = manager.get_all_drives_in_site()
for drive in drives:
    print(f"Drive Name: {drive.get('name')}, Drive ID: {drive.get('id')}")'''

# List the contents of the drive
#drive_id = "b!Sm5Rdoh1bUq94YPabsGWGuRxlSNtNf5JiFajd7jPnp67gLodnSjvQ7y2xdmZql36"
#contents = manager.list_drive_contents(drive_id)
#print("Drive Contents:", contents)
isLookingForFolder = True
if (isLookingForFolder):
    results = manager.search_folders_by_case_number(218444)
    for folder in results:
        print(folder)

else: 
    # Retrieve list items metadata
    metadata = manager.get_list_items_metadata(config("CLOUD_DOCS_SITE_ID"), config("CASE_FILES_LIST_ID"))
    print("Metadata:", metadata)

# List all available sites
#sites = manager.list_sites()
#print("Available Sites:", sites)

# List site contents
#site_contents = manager.list_site_contents()
#print("Available Sites:", site_contents)