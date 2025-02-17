from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from entries.models.medical_record import MedicalRecord
from entries.services import MedicalRecordStatusHandler
from integrations.services import SharePointManager

# Store old values before saving (for change tracking)
@receiver(pre_save, sender=MedicalRecord)
def track_old_values(sender, instance, **kwargs):
    if instance.pk: #Only tracks Updates, not New Entries
        try:
            old_instance = MedicalRecord.objects.get(pk=instance.pk)
            instance._old_values = old_instance.__dict__.copy()
        except MedicalRecord.DoesNotExist:
            instance._old_values = {}

# Handle new and updated entries
@receiver(post_save, sender=MedicalRecord)
def update_medical_record_status(sender, instance, created, **kwargs):
    MedicalRecordStatusHandler.update_status(instance)
        
# Handle deleted entries
@receiver(pre_delete, sender=MedicalRecord)
def handle_medical_record_delete(sender, instance, **kwargs):
    manager = SharePointManager()
    success = manager.delete_temp_folder(instance.temp_folder_id)
    if success:
        print(f"Medical Record deleted: {instance}. Client: {instance.client}")
