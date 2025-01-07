from core.onedrive import OneDriveManager

manager = OneDriveManager()
manager.authenticate()

# Create a folder
#result = manager.create_folder("Test Folder")
#print("Folder creation result:", result)

# List drives available
#drives = manager.list_drives()
#print("List of drives:", drives)

# List the contents of the drive
#drive_id = "b!Sm5Rdoh1bUq94YPabsGWGuRxlSNtNf5JiFajd7jPnp67gLodnSjvQ7y2xdmZql36"
#contents = manager.list_drive_contents(drive_id)
#print("Drive Contents:", contents)

# List all available sites
sites = manager.list_sites()
print("Available Sites:", sites)