import os
import sys

import django
from django.conf import settings
from django.test.utils import get_runner

os.environ["DJANGO_SETTINGS_MODULE"] = "tests.settings"


def runtests():
    """Set up test runner and run tests."""
    django.setup()

    TestRunner = get_runner(settings)

    test_runner = TestRunner()

    num_failures = test_runner.run_tests(["tests"])

    return num_failures


if __name__ == "__main__":
    num_failures = runtests()
    sys.exit(bool(num_failures))
