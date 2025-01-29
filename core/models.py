from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

# Create your models here.
class Location(models.Model):
    name = models.CharField(max_length=50, unique=True)
    abbreviation = models.CharField(max_length=10, unique=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'

class CustomGroup(Group):
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'
    
class CustomUser(AbstractUser):
    location = models.ForeignKey('Location', on_delete=models.SET_NULL, null=True, blank=True)

    groups = models.ManyToManyField(
        CustomGroup,
        related_name='customuser_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_permissions_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

class Client(models.Model):
    case_number = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    office = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, related_name='clients')
    paralegal = models.ManyToManyField(CustomUser, related_name='client_paralegal')
    attorney = models.ManyToManyField(CustomUser, related_name='client_attorney')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.case_number}"
    
    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'
    
class EntryType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Entry Type'
        verbose_name_plural = 'Entry Types'
    
class Status(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    entry_type = models.ManyToManyField(EntryType, related_name='statuses')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Status'
        verbose_name_plural = 'Statuses'

class MedicalRecord(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='medical_records')
    requester = models.ManyToManyField(CustomUser, related_name='medical_records')
    provider = models.CharField(max_length=255)
    facility = models.CharField(max_length=255)
    invoice_number = models.CharField(max_length=50)
    invoice_date = models.DateField()
    pages = models.IntegerField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True, related_name='medical_records')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client.name} : {self.invoice_number} : {self.cost}"
    
    class Meta:
        verbose_name = 'Medical Record'
        verbose_name_plural = 'Medical Records'