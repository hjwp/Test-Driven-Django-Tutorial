#!/usr/bin/python
try: import unittest2 as unittest #for Python <= 2.6
except: import unittest
import pexpect
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
    logfile = open('django_server_logfile.txt', 'w')
    django_server_process = pexpect.spawn(
            'python',
            args=['manage.py', 'runserver'],
            logfile=logfile

    )
    django_server_process.expect(
        'Quit the server with CONTROL-C'
    )
    print 'django test server running'


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

