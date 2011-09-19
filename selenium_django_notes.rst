
sudo pip install selenium
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



