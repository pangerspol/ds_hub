from decouple import config
from datetime import datetime
from entries.enum import MedicalRecordStatus
from integrations.services import SharePointManager
from integrations.services import PDFManager
from integrations.services import EmailService
from integrations.services import GoogleSheetManager

class MedicalRecordStatusHandler:
    @staticmethod
    def update_status(instance):
        # Saves old status to compare at the end and decide if we call the instance.save
        old_status = instance.status

        # Managers
        sharepoint_manager = SharePointManager()
        pdf_manager = PDFManager()
        email_manager = EmailService()
        google_sheet_manager = GoogleSheetManager()

        # Medical Record Status Logic
        match instance.status:
            # NEW ENTRY LOGIC
            case MedicalRecordStatus.NEW_ENTRY.name:
                print("Inside New Entry")
                if not instance.temp_folder_id:
                    success, temp_folder_id = sharepoint_manager.create_folder(instance.provider, instance.invoice_number, instance.client.name, instance.client.case_number, "Medical Records")

                    if success:
                        instance.temp_folder_id = temp_folder_id
                    else:
                        print("Failed to create temp folder")
                        return

                if instance.cost <= 50:
                    instance.status = MedicalRecordStatus.PENDING_PAYMENT.name
                else:
                    if not instance.skip_request:
                        subject = f"Approval Required: {instance.client.name}_{instance.client.case_number}"

                        if instance.notify_requester:
                            requester_email = [instance.requester.email]
                        else:
                            requester_email = []

                        if instance.notify_attorney and instance.client.attorney:
                            attorney_email = [instance.client.attorney.email]
                        else:
                            attorney_email = []

                        context = {
                            "client_name": instance.client.name,
                            "case_number": instance.client.case_number,
                            "provider": instance.provider.name,
                            "facility": instance.facility,
                            "invoice_number": instance.invoice_number,
                            "invoice_date": instance.invoice_date,
                            "quantity": instance.quantity,
                            "cost": instance.cost,
                            "office": instance.client.office.abbreviation
                        }

                        email_manager.send_email(
                            "approval_request", 
                            subject, 
                            [instance.client.paralegal.email],  # Must be a list (single recipient is fine)
                            context,
                            None,  # Uses default `from_email`
                            requester_email + attorney_email,  # Correctly merges into a flat list
                            None,
                            None
                        )
                    instance.status = MedicalRecordStatus.PENDING_APPROVAL.name

            # PENDING APPROVAL LOGIC
            case MedicalRecordStatus.PENDING_APPROVAL.name:
                print("Inside Pending Approval Logic")
                if instance.approval_path:
                    instance.status = MedicalRecordStatus.PENDING_PAYMENT.name
                if instance.is_denied:
                    instance.status = MedicalRecordStatus.DENIED.name

            # DENIED LOGIC
            case MedicalRecordStatus.DENIED.name:
                print("Inside Completed Logic")

                if not instance.is_denied:
                    pass #Cannot transition back to new entry without an invoice file
                    #instance.status = MedicalRecordStatus.NEW_ENTRY.name 
                    ##### IF WE GO BACK TO NEW_ENTRY FROM HERE THERE IS NO INVOICE FILE WHICH IS MANDATORY
                elif instance.temp_folder_id:
                    success = sharepoint_manager.delete_folder(instance.temp_folder_id)
                    if success:
                        instance.temp_folder_id = None
                        print(f"Medical Record deleted: {instance}. Client: {instance.client}")

            # PENDING PAYMENT LOGIC
            case MedicalRecordStatus.PENDING_PAYMENT.name:
                print("Inside Pending Payment Logic")
                if instance.receipt_path:
                    # Sets the custom name for the expense file
                    formated_date = instance.invoice_date.strftime("%y.%m.%d")
                    custom_name = f"{formated_date} {instance.provider} - {instance.facility} - Inv #{instance.invoice_number} - ${instance.cost} PAID"

                        # Checks to see if it has atty approval pdf
                    if instance.approval_path:
                        file_ids = [instance.invoice_file_id, instance.receipt_file_id, instance.approval_file_id]
                    else:
                        file_ids = [instance.invoice_file_id, instance.receipt_file_id]

                    # Tries to merge the pdfs - case expense
                    instance.expense_path, instance.expense_file_id = pdf_manager.merge_pdfs_from_sharepoint(file_ids, instance.temp_folder_id, "expense", custom_name)

                    # Checks to see if expense path is saved
                    if not instance.expense_path:
                        print("Could not retrieve expense path")
                        return
                    
                    sharepoint_manager.copy_file(instance.expense_file_id, instance.client.expense_folder_id)

                    data_list = [
                        instance.client.case_number,            #"Case Number"
                        instance.client.name,                   #"Client Name"
                        instance.provider.name,                 #"Provider"
                        instance.facility,                      #"Facility" 
                        instance.invoice_number,                #"Invoice" 
                        instance.quantity,                      #"Quantity" 
                        instance.is_cd,                         #"isCD"
                        float(instance.cost),                   #"Cost" 
                        instance.requester.username,            #"Requester" 
                        instance.client.paralegal.username,     #"Paralegal"
                        instance.client.office.name,            #"Office"
                        datetime.today().strftime("%Y-%m-%d"),  #"Date Paid"
                    ]

                    sheet_id = config("GOOGLE_SHEET_MR_PA_ID")
                    google_sheet_manager.log_payment(data_list, sheet_id, "Medical Records")
                    # Changes status from Pending Payment to Pending Records
                    instance.status = MedicalRecordStatus.PENDING_RECORDS.name

            # PENDING RECORDS LOGIC
            case MedicalRecordStatus.PENDING_RECORDS.name:
                print("Inside Pending Records Logic")
                if instance.skip_download:
                    # No need to email
                    instance.status = MedicalRecordStatus.COMPLETED.name

                if instance.record_path:
                    # Sets the custom name for the expense file
                    formated_date = instance.invoice_date.strftime("%y.%m.%d")
                    custom_name = f"{formated_date} {instance.provider.abbreviation} - {instance.facility} - Inv #{instance.invoice_number} - {instance.client.office.abbreviation} - {instance.client.name}_{instance.client.case_number} - ${instance.cost} PAID"
                    file_ids = [instance.expense_file_id, instance.record_file_id]
                    instance.package_path, instance.package_file_id = pdf_manager.merge_pdfs_from_sharepoint(file_ids, instance.temp_folder_id, "package", custom_name)
                    # Checks to see if expense path is saved
                    if not instance.package_path:
                        print("Could not retrieve package path")
                        return

                    sharepoint_manager.copy_file(instance.package_file_id, instance.client.lexviamail_folder_id)
                    print("5")
                    # Changes status from Pending Payment to Pending Records
                    instance.status = MedicalRecordStatus.COMPLETED.name

            # COMPLETED LOGIC
            case MedicalRecordStatus.COMPLETED.name: # Need to edit this so it only deletes the temp_folder if the package has been saved to client folder and the email confirmation has been sent out
                print("Inside Completed Logic")
                send_email = False
                if instance.package_path:
                    send_email = True
                if instance.temp_folder_id:
                    success = sharepoint_manager.delete_folder(instance.temp_folder_id)
                if success:
                    instance.temp_folder_id = None
                    instance.invoice_file_id = None
                    instance.approval_file_id = None
                    instance.receipt_file_id = None
                    instance.record_file_id = None
                    instance.package_file_id = None
                    print(f"Medical Record deleted: {instance}. Client: {instance.client}")

                    if send_email:
                        subject = f"Record Available for {instance.client.name}_{instance.client.case_number}"

                        if instance.notify_requester:
                            requester_email = [instance.requester.email]
                        else:
                            requester_email = []

                        if instance.notify_attorney and instance.client.attorney:
                            attorney_email = [instance.client.attorney.email]  # Ensure it's a list
                        else:
                            attorney_email = []

                        context = {
                            "client_name": instance.client.name,
                            "case_number": instance.client.case_number,
                            "provider": instance.provider.name,
                            "facility": instance.facility,
                            "invoice_number": instance.invoice_number,
                            "invoice_date": instance.invoice_date,
                            "quantity": instance.quantity,
                            "cost": instance.cost,
                            "office": instance.client.office.abbreviation
                        }

                        email_manager.send_email(
                            "completed", 
                            subject, 
                            [instance.client.paralegal.email],  # Must be a list (single recipient is fine)
                            context,
                            None,  # Uses default `from_email`
                            requester_email + attorney_email,  # Correctly merges into a flat list
                            None,
                            None
                        )


            # DEFAULT LOGIC
            case _:
                print("Inside Empty Match Logic") #Logic Here

        # Checks to see if there was an update to status and saves it
        if old_status != instance.status:
            instance.save()
        else:
            pass # IF no changes then pass to prevent recursion



        