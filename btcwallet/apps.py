from django.apps import AppConfig


class BtcwalletConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "btcwallet"

    def ready(self):
        import btcwallet.signals
