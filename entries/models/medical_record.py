from django.db import models
from core.models.client import Client
from core.models.auth import CustomUser
from core.models.provider import Provider
from entries.enum import MedicalRecordStatus

class MedicalRecord(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='medical_records')
    requester = models.ForeignKey(CustomUser, on_delete=models.PROTECT, null=True, blank=False, limit_choices_to={'groups__name': 'Requester'}, related_name='medical_records')

    provider = models.ForeignKey(Provider, on_delete=models.PROTECT, null=True, blank=False, related_name='medical_records')
    facility = models.CharField(max_length=255)
    invoice_number = models.CharField(max_length=50)
    invoice_date = models.DateField()
    quantity = models.IntegerField()
    is_cd = models.BooleanField(default=False)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    skip_request = models.BooleanField(default=False)
    notify_requester = models.BooleanField(default=True)
    notify_attorney = models.BooleanField(default=False)
    reply_to = models.BooleanField(default=False)

    last_approval_message_id = models.CharField(max_length=500, null=True, blank=True)

    temp_folder_id = models.CharField(max_length=500, null=True, blank=True)
    invoice_path = models.CharField(max_length=500, null=True,blank=True)
    approval_path = models.CharField(max_length=500, null=True,blank=True)
    receipt_path = models.CharField(max_length=500, null=True,blank=True)
    expense_path = models.CharField(max_length=500, null=True,blank=True)
    record_path = models.CharField(max_length=500, null=True,blank=True)
    package_path = models.CharField(max_length=500, null=True,blank=True)

    invoice_file_id = models.CharField(max_length=500, null=True,blank=True)
    approval_file_id = models.CharField(max_length=500, null=True,blank=True)
    receipt_file_id = models.CharField(max_length=500, null=True,blank=True)
    expense_file_id = models.CharField(max_length=500, null=True,blank=True)
    record_file_id = models.CharField(max_length=500, null=True,blank=True)
    package_file_id = models.CharField(max_length=500, null=True,blank=True)
    
    is_denied = models.BooleanField(default=False)
    skip_download = models.BooleanField(default=False)

    status = models.CharField(
        max_length=50,
        choices=[(status.name, status.value) for status in MedicalRecordStatus],
        default=MedicalRecordStatus.NEW_ENTRY.name
    )
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client.name} : {self.invoice_number} : {self.cost}"
    
    class Meta:
        verbose_name = 'Medical Record'
        verbose_name_plural = 'Medical Records'