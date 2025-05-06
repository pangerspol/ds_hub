from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from .models import Client, CustomUser, Location, CustomGroup, Provider
from entries.models.medical_record import MedicalRecord
from django.contrib.contenttypes.models import ContentType
from integrations.services import SharePointManager
from django.utils.html import format_html

class CustomAdminSite(admin.AdminSite):
    site_header = 'Dressler Strickland Hub'
    site_title = 'DS Hub - Admin Portal'
    index_title = 'Welcome to DS Hub Admin Portal'

    def get_app_list(self, request, app_label=None):
        app_list = super().get_app_list(request)
        for app in app_list:
            if app['app_label'] == 'core':
                app['models'].sort(key=lambda x: ['Provider', 'Location', 'CustomGroup', 'CustomUser', 'Client'].index(x['object_name']))
        return app_list

custom_admin_site = CustomAdminSite(name='custom_admin')

@admin.register(CustomUser, site=custom_admin_site)
class CustomUserAdmin(UserAdmin):
    # Fields to display in the admin list view
    list_display = ('id', 'username', 'email', 'location')
    # Fields to allow searching
    search_fields = ('username', 'email', 'first_name', 'last_name', 'location', 'groups')
    # Filters to display in the sidebar
    list_filter = ('groups', 'location')

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

@admin.register(Client, site=custom_admin_site)
class ClientAdmin(admin.ModelAdmin):
    form = ClientAdminForm
    list_display = ('id', 'case_number', 'name', 'paralegal', 'office')
    search_fields = ('case_number', 'name')
    list_filter = ('paralegal', 'office')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        manager = SharePointManager()
        
        if not obj.office:
            obj.office = obj.paralegal.location

        if not obj.main_folder_id:
            
            obj.main_folder_id, obj.sharepoint_url, obj.expense_folder_id, obj.lexviamail_folder_id = manager.search_folders_by_case_number(obj.case_number, ["Case Expenses", "Lexvia Mail"])
            if not obj.main_folder_id:
                print(f"Could not find a folder id for case#{obj.case_number} on CloudDocs")
                return
            obj.save()

class MedicalRecordAdminForm(forms.ModelForm):

    invoice_file = forms.FileField(required=False, label="Upload Invoice")
    approval_file = forms.FileField(required=False)
    receipt_file = forms.FileField(required=False)
    record_file = forms.FileField(required=False)
    class Meta:
        model = MedicalRecord
        fields = '__all__'

@admin.register(MedicalRecord, site=custom_admin_site)
class MedicalRecordAdmin(admin.ModelAdmin):
    form = MedicalRecordAdminForm
    list_display = ('id', 'client', 'get_paralegal', 'provider', 'facility', 'get_invoice', 'formatted_cost', 'get_office', 'formatted_status')
    search_fields = ('client__name', 'client__case_number', 'status', 'invoice_number', 'facility')
    list_filter = ('status', 'provider', 'facility', 'client__office', 'client__paralegal')

    def get_office(self, obj):
        return obj.client.office.abbreviation
    
    def formatted_cost(self, obj):
        return f"${obj.cost:.2f}"
    
    def formatted_status(self, obj):
        return obj.status.replace("_", " ").title()
    
    def get_paralegal(self, obj):
        return obj.client.paralegal.username
    
    def get_invoice(self, obj):
        return obj.invoice_number

    get_paralegal.short_description = "Paralegal"
    get_office.short_description = "Office"
    formatted_cost.short_description = "Cost"
    formatted_status.short_description = "Status"
    get_invoice.short_description = "Invoice"

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        manager = SharePointManager()
        if form.cleaned_data.get('invoice_file'):
            obj.invoice_path, obj.invoice_file_id = manager.upload_file(form.cleaned_data['invoice_file'], obj.temp_folder_id, "invoice")
            obj.save()
        if form.cleaned_data.get('approval_file'):
            obj.approval_path, obj.approval_file_id = manager.upload_file(form.cleaned_data['approval_file'], obj.temp_folder_id, "approval")
            obj.save()
        if form.cleaned_data.get('receipt_file'):
            if obj.approval_path or obj.cost <= 50:
                obj.receipt_path, obj.receipt_file_id = manager.upload_file(form.cleaned_data['receipt_file'], obj.temp_folder_id, "receipt")
                obj.save()
            else:
                print("Cannot upload receipt without attorney approval")
        if form.cleaned_data.get('record_file'):
            obj.record_path, obj.record_file_id = manager.upload_file(form.cleaned_data['record_file'], obj.temp_folder_id, "record")
            obj.save()

@admin.register(Location, site=custom_admin_site)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'abbreviation', 'address', 'phone_number', 'email', 'is_active')
    search_fields = ('name', 'abbreviation', 'address', 'phone_number', 'email')
    list_filter = ('is_active',)

class ProviderAdminForm(forms.ModelForm):
    class Meta:
        model = Provider
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["entry_type"].queryset = ContentType.objects.filter(app_label='entries')
        self.fields["entry_type"].label_from_instance = lambda obj: obj.__str__().replace("Entries | ", "")

@admin.register(Provider, site=custom_admin_site)
class ProviderAdmin(admin.ModelAdmin):
    form = ProviderAdminForm
    list_display = ('id', 'name', 'abbreviation', 'website', 'request_portal')
    search_fields = ('name', 'abbreviation')
    list_filter = ('is_active',)
