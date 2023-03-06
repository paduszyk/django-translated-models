from django.test import TestCase

from .models import Movie


class TestTranslatedModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.model = Movie
        cls.original = {
            attr: getattr(cls.model, attr)
            for attr in ("translated_fields", "languages")
        }

    def model_reset(self):
        for attr, value in self.original.items():
            setattr(self.model, attr, value)

    def model_update(self, **kwargs):
        for attr, value in kwargs.items():
            setattr(self.model, attr, value)

    def assertModelCheckFailsWithMessageCode(self, message_id):
        messages = self.model.check()
        self.assertTrue(
            message_id in [message.id for message in messages],
            msg=f"Check did not fail with {message_id}.",
        )

    def setUp(self):
        self.model_reset()

    def test_get_translated_fields_translated_fields_none(self):
        self.assertSetEqual(
            set(self.model.get_translated_fields()), {"title", "genre"}
        )

    def test_get_translated_fields_translated_fields_given(self):
        self.model_update(translated_fields=["title"])
        self.assertEqual(self.model.get_translated_fields(), ["title"])

    def test_get_languages_languages_none(self):
        self.assertSetEqual(set(self.model.get_languages()), {"en", "pl"})

    def test_get_languages_languages_given(self):
        self.model_update(languages=["en", "pl"])
        self.assertSetEqual(set(self.model.get_languages()), {"en", "pl"})

    def test_check_model_fails_with_E002(self):
        # Invalid type for the `translated_fields` attribute
        self.model_update(translated_fields=0)
        self.assertModelCheckFailsWithMessageCode("translated_models.E002")

    def test_check_model_fails_with_E003(self):
        # Non-existing field name in the `translated_fields` attribute
        self.model_update(translated_fields=["actors"])
        self.assertModelCheckFailsWithMessageCode("translated_models.E003")

    def test_check_model_fails_with_E004(self):
        # Unsupported field type in the `translated_fields` attribute
        self.model_update(translated_fields=["premiere_date"])
        self.assertModelCheckFailsWithMessageCode("translated_models.E004")

    def test_check_model_fails_with_E005(self):
        # Invalid type for the `languages` attribute
        self.model_update(languages=0)
        self.assertModelCheckFailsWithMessageCode("translated_models.E005")

    def test_check_model_fails_with_E006(self):
        # Non-existing language code in the `languages` attribute
        self.model_update(languages=["xy"])
        self.assertModelCheckFailsWithMessageCode("translated_models.E006")

    def test_check_model_fails_with_E007(self):
        # Language not set in settings module in the `languages` attribute
        self.model_update(languages=["de"])
        self.assertModelCheckFailsWithMessageCode("translated_models.E007")

    def test_check_model_fails_with_E008(self):
        # None value for the `original_language` attribute
        self.model_update(original_language=None)
        self.assertModelCheckFailsWithMessageCode("translated_models.E008")

    def test_check_model_fails_with_E009(self):
        # Non-string value for the `original_language` attribute
        self.model_update(original_language=0)
        self.assertModelCheckFailsWithMessageCode("translated_models.E009")

    def test_check_model_fails_with_E010(self):
        # Non-existing language code for the `original_language` attribute
        self.model_update(original_language="xy")
        self.assertModelCheckFailsWithMessageCode("translated_models.E010")

    def test_check_model_fails_with_E011(self):
        # Language not set in settings module in the `languages` attribute
        self.model_update(original_language="de")
        self.assertModelCheckFailsWithMessageCode("translated_models.E011")
