from django.apps import AppConfig


class DronoviappConfig(AppConfig):
    name = 'DronoviApp'
    def ready(self):
        import DronoviApp.signals
