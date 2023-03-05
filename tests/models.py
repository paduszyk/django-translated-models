from django.db import models

from translated_models.models import TranslatedModel


class Movie(TranslatedModel):
    """An example of concrete model based on `TranslatedModel`."""

    # Translatable fields
    title = models.TextField()
    genre = models.CharField(max_length=255)

    # Non-translatable fields
    premiere_date = models.DateTimeField()

    # Model attributes set to their defaults. They are overridden individually
    # in tests depending on a being feature tested.

    class Meta:
        app_label = "tests"
