from django.db import models

# Create your models here.

class Request(models.Model):
    case_number = models.CharField(max_length=50)
    client_name = models.CharField(max_length=100)
    paralegal = models.CharField(max_length=100)
    office = models.CharField(max_length=50, choices=[('Hartford', 'Hartford'), ('Waterbury', 'Waterbury')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.case_number} - {self.client_name}"