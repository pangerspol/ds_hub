from core.onedrive import OneDriveManager

manager = OneDriveManager()
manager.authenticate()

#result = manager.create_folder("Test Folder")
#print("Folder creation result:", result)

drives = manager.list_drives()
print("List of drives:", drives)