OBIDIRE ALLA CAPRA! - Un tutorial TDD con Selenium e Django
===========================================================

*Harry Percival*
@hjwp
https://www.obeythetestinggoat.com
https://www.pythonanywhere.com


















Introduzione
------------

* l'Italiano
* l'Inglese
* linguagio technico
* **le domande, per preghiera** 
   - non fare sempre "si"
   - e anche le correzione del' Italiano





















Voi
---

* chi conosce Django? Python? TDD? Selenium?

Io
--

* Sestri Levante
* il primo progetto
* Resolver Systems & PythonAnywhere
* il libero















Oggi
----

* Come s'inizia il TDD, da 0
* passare a unittest
* test unitari per pagine - tests.py, urls.py, views.py
* forse -- passare al Django Test Client, templates



useful commands::

    vi functional_tests.py
    python functional_tests.py
    django-admin.py startproject superlists
    cd superlists
    mv ../functional_tests.py .

    git init .
    git add functional_tests.py manage.py superlists/*.py
    git commit -m"initial commit"

    git remote add repo ~/Dropbox/book/source/chapter_9/superlists
    git fetch repo
    git checkout repo/chapter_3 -- functional_tests.py

    python functional_tests.py 
    python manage.py startapp lists
    vi lists/tests.py

    git checkout repo/chapter_3 -- lists/tests.py
    git checkout repo/chapter_3 -- superlists/settings.py

    python manage.py test lists
    vi lists/tests.py
    python manage.py test lists
    python manage.py runserver &
    python functional_tests.py 
    vi functional_tests.py 

    git checkout repo/chapter_3_switch_to_django_test_client -- lists/tests.py


