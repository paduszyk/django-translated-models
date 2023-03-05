from django.test import TestCase, override_settings

from translated_models.utils import (
    is_field_translatable,
    is_language_in_django,
    is_language_in_settings,
)

from .models import Movie


@override_settings(
    LANGUAGES=[
        ("en", "English"),
        ("pl", "Polish"),
        ("fr", "French"),
    ]
)
class Tests(TestCase):
    def test_is_language_in_django_valid_code(self):
        self.assertTrue(is_language_in_django("en-us"))

    def test_is_language_in_django_invalid_code(self):
        self.assertFalse(is_language_in_django("xy"))

    def test_is_language_in_settings_valid_code(self):
        self.assertTrue(is_language_in_settings("en-us"))

    def test_is_language_in_settings_invalid_code(self):
        self.assertFalse(is_language_in_settings("de"))

    def test_is_field_translatable_valid_field(self):
        field = Movie._meta.get_field("title")
        self.assertTrue(is_field_translatable(field))

    def test_is_field_translatable_invalid_field(self):
        field = Movie._meta.get_field("premiere_date")
        self.assertFalse(is_field_translatable(field))
