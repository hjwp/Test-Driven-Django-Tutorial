
sudo pip install selenium
sudo pip install pexpect

wget -O selenium-server-standalone-2.6.0.jar http://selenium.googlecode.com/files/selenium-server-standalone-2.6.0.jar 

django-admin startproject mysite

edit settings.py - set database

syncdb

startapp polls


first test:  the django admin

mkdir functional_tests
touch __init__.py

create run_functional_tests.py
add test_admin.py
chmod run_functional_test.py

rm polls/tests.py
mkdir polls/tests
touch polls/tests/__init__.py

from test_models import *

test_models.py
models.py

first test 



