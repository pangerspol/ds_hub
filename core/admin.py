from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from .models import Client, EntryType, Status, MedicalRecord, CustomUser, Location, CustomGroup
class CustomAdminSite(admin.AdminSite):
    site_header = 'Dressler Strickland Hub'
    site_title = 'DS Hub - Admin Portal'
    index_title = 'Welcome to DS Hub Admin Portal'

    def get_app_list(self, request, app_label=None):
        app_list = super().get_app_list(request)
        for app in app_list:
            if app['app_label'] == 'core':
                app['models'].sort(key=lambda x: ['CustomUser', 'CustomGroup', 'Location', 'EntryType', 'Status', 'Client', 'MedicalRecord'].index(x['object_name']))
        return app_list

custom_admin_site = CustomAdminSite(name='custom_admin')

@admin.register(CustomUser, site=custom_admin_site)
class CustomUserAdmin(UserAdmin):
    # Fields to display in the admin list view
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'location')
    # Fields to allow searching
    search_fields = ('username', 'email', 'first_name', 'last_name')
    # Filters to display in the sidebar
    list_filter = ('is_staff', 'is_superuser', 'groups')

    # Fieldsets for organizing fields in the admin form
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'location')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Fields to include when creating a new user via the admin panel
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'location'),
        }),
    )

    # Default ordering
    ordering = ('username',)

@admin.register(CustomGroup, site=custom_admin_site)
class CustomGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active')
    search_fields = ('name',)
    list_filter = ('is_active',)

class ClientAdminForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['paralegal'].queryset = CustomUser.objects.filter(groups__name='Paralegal')
        self.fields['attorney'].queryset = CustomUser.objects.filter(groups__name='Attorney')

@admin.register(Client, site=custom_admin_site)
class ClientAdmin(admin.ModelAdmin):
    form = ClientAdminForm
    list_display = ('id', 'case_number', 'name')  # Replace with relevant fields
    search_fields = ('case_number', 'name', 'email')


@admin.register(EntryType, site=custom_admin_site)
class EntryTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Status, site=custom_admin_site)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

class MedicalRecordAdminForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['requester'].queryset = CustomUser.objects.filter(groups__name='Requesters')

@admin.register(MedicalRecord, site=custom_admin_site)
class MedicalRecordAdmin(admin.ModelAdmin):
    form = MedicalRecordAdminForm
    list_display = ('client', 'invoice_number', 'cost', 'provider', 'status')
    search_fields = ('client_name', 'status_name')
    list_filter = ('status', 'invoice_number')
    ordering = ('invoice_number',)

@admin.register(Location, site=custom_admin_site)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'abbreviation', 'address', 'phone_number', 'email', 'is_active')
    search_fields = ('name', 'abbreviation', 'address', 'phone_number', 'email')
    list_filter = ('is_active',)