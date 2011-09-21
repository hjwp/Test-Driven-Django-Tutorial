#!/usr/bin/python
import pexpect
import unittest


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
    django_server_process = pexpect.spawn(
            'python',
            args=['manage.py', 'runserver']
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

