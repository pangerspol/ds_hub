from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

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