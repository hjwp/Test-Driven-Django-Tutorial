#!/usr/bin/python
try: import unittest2 as unittest #for Python <= 2.6
except: import unittest
import json
from selenium import webdriver
import subprocess
from tempfile import NamedTemporaryFile


ADMIN_USER_DICT = {
    "pk": 1,
    "model": "auth.user",
    "fields": {
        "username": "admin",
        "is_active": True,
        "is_superuser": True,
        "is_staff": True,
        "password": r"sha1$c6584$b8a0656080944eed8e0db23e3aa6e690f255aa52",
        "email": "admin@example.com",
        "date_joined": "2011-10-13 09:13:23"
    }
}

ROOT = 'http://127.0.0.1:8000'


class FunctionalTest(unittest.TestCase):

    def setUp(self):
        reset_database()
        self.django = start_django_server()
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(5)


    def tearDown(self):
        self.browser.close()
        self.django.kill()



def run_syncdb():
    print 'running syncdb'
    subprocess.Popen(
            ['python', 'manage.py', 'syncdb', '--noinput', '--settings=settings_for_fts']
    ).communicate()


def start_django_server():
    print '(re) starting django test server'
    #noreload ensures single process
    django_server = subprocess.Popen(
            ['python', 'manage.py', 'runserver', '--noreload', '--settings=settings_for_fts']
    )
    #dev server starts quickly, no need to check it's running
    return django_server


def reset_database():
    print 'flushing database'
    subprocess.Popen(
        ['python', 'manage.py', 'flush', '--noinput', '--settings=settings_for_fts']
    ).communicate()
    print 'loading fixtures'
    with NamedTemporaryFile(delete=False) as temp:
        fixture_json = json.dumps([ADMIN_USER_DICT])
        temp.write(fixture_json)
        temp.seek(0)
        print temp.read()
        temp.seek(0)
        subprocess.Popen(
            ['python', 'manage.py', 'loaddata', temp.name, '--settings=settings_for_fts']
        ).communicate()

    print 'fixtures loaded from', temp.name


def run_all_functional_tests():
    print 'running tests'
    tests = unittest.defaultTestLoader.discover('fts')
    runner = unittest.TextTestRunner()
    runner.run(tests)





if __name__ == '__main__':
    run_syncdb()
    run_all_functional_tests()
