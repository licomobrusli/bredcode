from django.apps import AppConfig
import logging

class ConfigAppConfig(AppConfig):
    name = 'config'

    def ready(self):
        logger = logging.getLogger(__name__)
        logger.info('Config app is starting up.')  # Test message
        import config.signals  # Assuming this is correct
