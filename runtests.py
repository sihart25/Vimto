#!/usr/bin/env python
import os
import sys

import django
from django.conf import settings
from django.test.utils import get_runner

if __name__ == "__main__":
    os.environ['DJANGO_SETTINGS_MODULE'] = 'vimto.settings'
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    settings.TESTMODE = True
    failures = test_runner.run_tests([
        # 'auth_test.tests',
        'vimto_ws.tests',
        'vimto_auth.tests',
        'vimto.tests'])
    sys.exit(bool(failures))