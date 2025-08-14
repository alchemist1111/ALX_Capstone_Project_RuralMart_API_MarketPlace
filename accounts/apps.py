from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
    
    def ready(self):
        # Import signals to ensure they are registered
        import accounts.signals
        # Ensure signals are imported when the app is ready
        print("Accounts app is ready and signals are imported.")
