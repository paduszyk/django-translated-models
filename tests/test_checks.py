from django.conf import global_settings
from django.test import TestCase, override_settings

from translated_models import checks


class TestChecks(TestCase):
    def assertCheckFailsWithMessageCode(self, check, message_id):
        messages = check(app_configs=None)
        self.assertTrue(
            message_id in [message.id for message in messages],
            msg=f"Check did not fail with {message_id}.",
        )

    @override_settings(
        LANGUAGES=global_settings.LANGUAGES,
    )
    def test_check_settings_fails_with_E001(self):
        self.assertCheckFailsWithMessageCode(
            checks.check_settings, "translated_models.E001"
        )
