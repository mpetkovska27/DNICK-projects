from django.apps import AppConfig


class NedvizninaappConfig(AppConfig):
    name = 'NedvizninaApp'
    def ready(self):
        import NedvizninaApp.signals
