from django.db import models
from django.contrib.contenttypes.models import ContentType

class Provider(models.Model):
    name = models.CharField(max_length=50, unique=True)
    aka = models.CharField(max_length=50, null=True, unique=True)
    abbreviation = models.CharField(max_length=10, unique=True)
    website = models.URLField(blank=True, null=True)
    request_portal = models.URLField(blank=True, null=True)
    payment_portal = models.URLField(blank=True, null=True)
    records_portal = models.URLField(blank=True, null=True)
    other_portal = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    entry_type = models.ManyToManyField(ContentType, related_name='providers')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Provider'
        verbose_name_plural = 'Providers'