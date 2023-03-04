import os

from django.conf import global_settings, settings
from django.core.checks import Error, Tags, register

django_languages = global_settings.LANGUAGES


@register(Tags.translation)
def check_settings(app_configs, **kwargs):
    errors = []

    if settings.LANGUAGES == django_languages:
        errors.append(
            Error(
                "LANGUAGES setting isn't set in {} module.".format(
                    os.environ["DJANGO_SETTINGS_MODULE"]
                ),
                id="translated_models.E001",
            )
        )

    return errors
