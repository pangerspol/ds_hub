#from core.models import Status
from entries.enum import MedicalRecordStatus
from integrations.services import SharePointManager
from integrations.services import PDFManager

class MedicalRecordStatusHandler:
    @staticmethod
    def update_status(instance):
        # Saves old status to compare at the end and decide if we call the instance.save
        old_status = instance.status

        # Managers
        sharepoint_manager = SharePointManager()
        pdf_manager = PDFManager()

        # Medical Record Status Logic
        match instance.status:
            # NEW ENTRY LOGIC
            case MedicalRecordStatus.NEW_ENTRY.name:
                print("Inside New Entry")
                if not instance.temp_folder_id:
                    success, temp_folder_id = sharepoint_manager.create_temp_folder(instance.provider, instance.invoice_number, instance.client.name, instance.client.case_number)

                    if success:
                        instance.temp_folder_id = temp_folder_id
                    else:
                        print("Failed to create temp folder")
                        return

                if instance.cost <= 50:
                    instance.status = MedicalRecordStatus.PENDING_PAYMENT.name
                else:
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
                    success = sharepoint_manager.delete_temp_folder(instance.temp_folder_id)
                    if success:
                        instance.temp_folder_id = None
                        print(f"Medical Record deleted: {instance}. Client: {instance.client}")

            # PENDING PAYMENT LOGIC
            case MedicalRecordStatus.PENDING_PAYMENT.name:
                print("Inside Pending Payment Logic")
                if instance.receipt_path:
                    # Sets the custom name for the expense file
                    custom_name = f"{instance.provider} - Inv #{instance.invoice_number}_{instance.client.case_number} - ${instance.cost} PAID"

                    # Checks to see if it has atty approval pdf
                    if instance.approval_path:
                        pdf_urls = [instance.invoice_path, instance.receipt_path, instance.approval_path]
                    else:
                        pdf_urls = [instance.invoice_path, instance.receipt_path]

                    # Checks to see if it has atty approval pdf
                    if instance.approval_path:
                        file_names = ["invoice.pdf", "receipt.pdf", "approval.pdf"]
                    else:
                        file_names = ["invoice.pdf", "receipt.pdf"]

                        # Checks to see if it has atty approval pdf
                    if instance.approval_path:
                        file_ids = [instance.invoice_file_id, instance.receipt_file_id, instance.approval_file_id]
                    else:
                        file_ids = [instance.invoice_file_id, instance.receipt_file_id]

                    # Tries to merge the pdfs
                    instance.expense_path, instance.expense_file_id = pdf_manager.merge_pdfs_from_sharepoint(file_ids, instance.temp_folder_id, "expense", custom_name)

                    # Checks to see if expense path is saved
                    if not instance.expense_path:
                        print("Could not retrieve expense path")
                        return
                    
                    # Changes status from Pending Payment to Pending Records
                    instance.status = MedicalRecordStatus.PENDING_RECORDS.name

            # PENDING RECORDS LOGIC
            case MedicalRecordStatus.PENDING_RECORDS.name:
                print("Inside Pending Records Logic")
                if instance.record_path or instance.skip_download:
                    instance.status = MedicalRecordStatus.COMPLETED.name

            # COMPLETED LOGIC
            case MedicalRecordStatus.COMPLETED.name:
                print("Inside Completed Logic")
                success = sharepoint_manager.delete_temp_folder(instance.temp_folder_id)
                if success:
                    instance.temp_folder_id = None
                    print(f"Medical Record deleted: {instance}. Client: {instance.client}")

            # DEFAULT LOGIC
            case _:
                print("Inside Empty Match Logic") #Logic Here

        # Checks to see if there was an update to status and saves it
        if old_status != instance.status:
            instance.save()
        else:
            pass # IF no changes then pass to prevent recursion



        