from django.apps import AppConfig


class CakeappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'CakeApp'

    def ready(self):
        import CakeApp.signals
