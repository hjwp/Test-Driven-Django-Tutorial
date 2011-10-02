#!/usr/bin/python
try: import unittest2 as unittest #for Python <= 2.6
except: import unittest
import pexpect
import subprocess
from selenium import webdriver


def start_selenium_server():
    print 'Starting Selenium'
    selenium_server_process = pexpect.spawn(
        'java',
        args=['-jar', 'selenium-server-standalone-2.6.0.jar']
    )
    selenium_server_process.expect(
        'Started org.openqa.jetty.jetty.Server'
    )
    print 'selenium started'


def start_django_server():
    print 'starting django test server'
    subprocess.Popen('python manage.py runserver', shell=True)
    #dev server starts quickly, no need to check it's running
    print 'django test server started'


def run_all_functional_tests():
    print 'running tests'
    tests = unittest.defaultTestLoader.discover('fts')
    runner = unittest.TextTestRunner()
    runner.run(tests)


if __name__ == '__main__':
    start_selenium_server()
    start_django_server()
    run_all_functional_tests()


ROOT = 'http://127.0.0.1:8000'

class FunctionalTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(5)

    def tearDown(self):
        self.browser.close()

