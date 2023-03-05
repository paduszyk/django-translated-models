from django.conf import settings
from django.db.models import CharField, TextField

if not hasattr(
    settings, "TRANSLATED_MODELS_TRANSLATABLE_FIELDS"
):  # pragma: no cover
    settings.TRANSLATED_MODELS_TRANSLATABLE_FIELDS = (CharField, TextField)
