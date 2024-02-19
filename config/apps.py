from django.apps import AppConfig

class ConfigAppConfig(AppConfig):
    name = 'config'

    def ready(self):
        import config.signals
