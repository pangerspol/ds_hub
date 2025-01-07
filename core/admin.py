from django.contrib import admin
from .models import Request

# Register your models here.

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('case_number', 'client_name', 'paralegal', 'office', 'created_at')
