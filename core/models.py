from django.db import models

class Request(models.Model):
    case_number = models.CharField(max_length=50)
    client_name = models.CharField(max_length=100)
    paralegal = models.CharField(max_length=100)
    office = models.CharField(max_length=50, choices=[('H', 'Hartford'), ('W', 'Waterbury'), ('O', 'Other')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request {self.case_number} - {self.client_name}"
    
class File(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE, related_name='files')
    file_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=50, choices=[('Invoice', 'Invoice'), ('Receoipt', 'Receipt')])
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file_type} for {self.request.case_number}"

class Document(models.Model):
    title = models.CharField(max_length=200)
    upload = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

# Create your models here.
