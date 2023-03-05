import os

from django.conf import settings
from django.core.checks import Error
from django.core.exceptions import FieldDoesNotExist
from django.db import models
from django.utils.text import get_text_list

from .utils import (
    is_field_translatable,
    is_language_in_django,
    is_language_in_settings,
)


class TranslatedModelQuerySet(models.QuerySet):
    """Database lookup for a set of translated objects."""


class TranslatedModelManager(
    models.Manager.from_queryset(queryset_class=TranslatedModelQuerySet)
):
    """Default manager of translated objects."""


class TranslatedModelBase(models.Model):
    """Base class to represent translated objects."""

    objects = TranslatedModelManager()

    # A collection (list, tuple, or set) of names for the model fields, for
    # which translation fields are created and appended to the model. If None,
    # all the CharFields and TextFields
    translated_fields = None

    # A collection (list, tuple, or set) of languages codes, for which
    # translation fields are created. If None, all the languages from the
    # LANGUAGES setting are used.
    languages = None

    class Meta:
        abstract = True

    @classmethod
    def get_translated_fields(cls):
        """Return a collection of translation fields."""
        translated_fields = cls.translated_fields
        if translated_fields is None:
            return [
                field.name
                for field in cls._meta.get_fields()
                if is_field_translatable(field)
            ]
        return translated_fields

    @classmethod
    def get_languages(cls):
        """Return a collection of translation languages used in the model."""
        languages = cls.languages
        if languages is None:
            languages = [code for code, name in settings.LANGUAGES]
        return [language.replace("-", "_") for language in languages]

    @classmethod
    def check(cls, **kwargs):
        """Perform a full model check."""
        errors = [
            *cls._check_translated_fields(**kwargs),
            *cls._check_languages(**kwargs),
        ]
        return errors

    @classmethod
    def _check_translated_fields(cls, **kwargs):
        """Perform `translated_fields` model attribute check."""
        errors = []

        translated_fields = cls.translated_fields
        if translated_fields is None:
            # Do not perform any further checks. The attribute's value is
            # handled by `get_translated_fields()` class method.
            return errors

        # Check if the attribute is of a valid type
        if not (
            isinstance(translated_fields, (list, tuple, set))
            and len(translated_fields) > 0
            and all(
                isinstance(translated_field, str)
                for translated_field in translated_fields
            )
        ):
            errors += [
                Error(
                    "'translated_fields' must be NoneType or a non-empty "
                    "collection (list, tuple, or set) of strings.",
                    obj=cls,
                    id="translated_models.E002",
                )
            ]

        # Check if all the attribute's values represent valid field name
        if not errors:
            for index, name in enumerate(translated_fields):
                try:
                    cls._meta.get_field(name)
                except FieldDoesNotExist:
                    errors += [
                        Error(
                            "translated_fields[{}] = '{}' doesn't represent "
                            "a name of any model's field.".format(index, name),
                            obj=cls,
                            id="translated_models.E003",
                        )
                    ]

        # Check if all the attribute's values represent translatable field
        if not errors:
            translatable_fields = (
                settings.TRANSLATED_MODELS_TRANSLATABLE_FIELDS
            )
            errors += [
                Error(
                    "translated_fields[{}] = '{}' doesn't represent a name of "
                    "translatable field. Currently, only fields of the "
                    "following type(s) are supported: {}.".format(
                        index,
                        name,
                        get_text_list(
                            [
                                f"{field.__module__}.{field.__name__}"
                                for field in translatable_fields
                            ],
                            last_word="and",
                        ),
                    ),
                    obj=cls,
                    id="translated_models.E004",
                )
                for index, name in enumerate(translated_fields)
                if not is_field_translatable(cls._meta.get_field(name))
            ]

        return errors

    @classmethod
    def _check_languages(cls, **kwargs):
        """Perform `languages` model attribute check."""
        errors = []

        languages = cls.languages
        if languages is None:
            # Do not perform any further checks. The attribute's value is
            # handled by `get_languages()` class method.
            return errors

        # Check if the attribute is of a valid type
        if not (
            isinstance(languages, (list, tuple, set))
            and len(languages) > 0
            and all(isinstance(language, str) for language in languages)
        ):
            errors += [
                Error(
                    "'languages' must be None or a non-empty collection "
                    "(list, tuple, or set) of strings.",
                    obj=cls,
                    id="translated_models.E005",
                )
            ]

        # Check if all the attribute's values represent a language code
        # available in the Django's global settings module
        if not errors:
            errors += [
                Error(
                    "languages[{}] = '{}' isn't a valid code for any of "
                    "languages available in Django.".format(index, code),
                    obj=cls,
                    id="translated_models.E006",
                )
                for index, code in enumerate(languages)
                if not is_language_in_django(code)
            ]

        # Check if all the attribute's values represent a language code
        # declared in the LANGUAGES setting of the settings module
        if not errors:
            errors += [
                Error(
                    (
                        "languages[{}] = '{}' doesn't represent a code for "
                        "any of language defined the LANGUAGES setting in {} "
                        "module."
                    ).format(
                        index, code, os.environ["DJANGO_SETTINGS_MODULE"]
                    ),
                    obj=cls,
                    id="translated_models.E007",
                )
                for index, code in enumerate(languages)
                if not is_language_in_settings(code)
            ]

        return errors


class TranslatedModel(TranslatedModelBase):
    """A class to represent translated objects.

    Concrete models should inherit directly from this class.
    """

    class Meta:
        abstract = True
