import logging
from django.apps import AppConfig

logger = logging.getLogger(__name__)

class ColorizerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'colorizer'

    def ready(self):
        """
        Load the colorization model when the Django app starts.
        
        This ensures the heavy model (110MB) is loaded only once at startup
        rather than on each request, improving performance significantly.
        """
        try:
            from .ml.services import colorization_service
            logger.info("Loading colorization model at app startup...")
            colorization_service.load_model()
            logger.info("Colorization model loaded successfully at startup")
            
        except Exception as e:
            logger.error(f"Failed to load colorization model at startup: {e}")
            # Don't crash the app if model loading fails
            # The view will handle the error gracefully
