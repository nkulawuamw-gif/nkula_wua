from django.apps import AppConfig


class AccountingAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounting_app"

    def ready(self):
        import accounting_app.signals
