from django.db import models

class Document(models.Model):
    title = models.CharField(max_length=200)
    upload = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

# Create your models here.
