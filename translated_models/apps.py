from django import apps


class TranslatedModelsConfig(apps.AppConfig):
    """A class representing the `translated_models` app configuration."""

    name = "translated_models"

    def ready(self):
        pass
