from django.conf import global_settings, settings


def _is_language_in_languages_settings(code, settings):
    """Return a boolean indicating whether the language of a given code is
    available in LANGUAGES setting of the settings module given."""
    codes, names = zip(*settings.LANGUAGES)
    return code.split("-")[0] in codes


def is_language_in_django(code):
    return _is_language_in_languages_settings(code, global_settings)


def is_language_in_settings(code):
    return _is_language_in_languages_settings(code, settings)


def is_field_translatable(field):
    """Return a boolean indicating whether field is "translatable", in other
    words, can be declared as the field to be translated."""
    return isinstance(
        field, (*settings.TRANSLATED_MODELS_TRANSLATABLE_FIELDS,)
    )
