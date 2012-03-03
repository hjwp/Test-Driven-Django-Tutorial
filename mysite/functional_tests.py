#!/usr/bin/env python
try: import unittest2 as unittest #for Python <= 2.6
except: import unittest
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import subprocess
import sys

import settings_for_fts
from django.core.management import call_command, setup_environ
setup_environ(settings_for_fts)
from django.contrib.auth.models import User
from django.conf import settings

# determine the root of the server
if hasattr(settings, 'ROOT'):
    ROOT = settings.ROOT
else:
    ROOT = 'http://localhost:8001'

class FunctionalTest(unittest.TestCase):

    def setUp(self):
        reset_database()
        # restart django server each test, because otherwise it doesn't see the
        # effects of resetting the db
        self.django = start_django_server()
        # Use a remote driver if setup
        if hasattr(settings, 'REMOTE_DRIVER_URL'):
            self.browser = webdriver.Remote(command_executor=settings.REMOTE_DRIVER_URL,
                                            desired_capabilities=DesiredCapabilities.FIREFOX)
        else:
            self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(5)


    def tearDown(self):
        self.browser.close()
        self.django.kill()



def run_syncdb():
    call_command('syncdb', interactive=False)


def start_django_server():
    #noreload ensures single process
    return subprocess.Popen([
            'python', 'manage.py', 'runserver',
            ROOT.replace('http://', ''), '--noreload', '--settings=settings_for_fts',
    ])


def reset_database():
    call_command('flush', interactive=False)
    admin = User(username='admin',is_staff=True, is_superuser=True, email='admin@example.com')
    admin.save()
    admin.set_password('adm1n')
    admin.save()


def run_functional_tests(pattern=None):
    print 'running tests'
    if pattern is None:
        tests = unittest.defaultTestLoader.discover('fts')
    else:
        pattern_with_globs = '*%s*' % (pattern,)
        tests = unittest.defaultTestLoader.discover('fts', pattern=pattern_with_globs)

    runner = unittest.TextTestRunner()
    runner.run(tests)





if __name__ == '__main__':
    run_syncdb()
    if len(sys.argv) == 1:
        run_functional_tests()
    else:
        run_functional_tests(pattern=sys.argv[1])
