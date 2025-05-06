from django.apps import AppConfig


class EntriesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'entries'

    def ready(self):
        import entries.signals.medical_record_signals # Loads Medical Record Signals
