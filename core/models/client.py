from django.db import models
from core.models.auth import CustomUser
from core.models.location import Location

class Client(models.Model):
    case_number = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    paralegal = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'groups__name': 'Paralegal'}, related_name="paralegal_client")
    attorney = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'groups__name': 'Attorney'}, related_name="attorney_client")
    office = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.case_number}"
    
    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'