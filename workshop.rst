WELCOME TO THE TEST-DRIVEN-DJANGO WORKSHOP
==========================================

Required installations
----------------------

 - Python (2.7 if poss, 2.6 otherwise)
 - Git
 - Firefox
 - Django (easy_install) 
 - Selenium (easy_install)
 - unittest2 # if on Python 2.6 (easy_install)

Checkout
--------

checkout the base repo::

   git clone --branch workshop https://github.com/hjwp/Test-Driven-Django-Tutorial.git
   git fetch --tags
   git checkout PART1







Introduction
============

Who I am, and why should you listen to me?
------------------------------------------

    - recent convert, resolver, etc


Who knows what?
---------------

    - Python - anyone v. new to it?

    - Django - anyone never used it?

    - TDD - unittest
 
    - Selenium


Laptops, tools and working
--------------------------

    - who is on Windows? Mac? Linux? VM? headless?? (the last is bad)

    - who is using an IDE?



The Plan
--------

    - To run through contents of official Django tutorial
        - ie, a polls/voting app
        - but TDD all the way

    - PART 1: Basic setup & the Django admin site
        - first selenium FT
        - first unit tests
        - models.py, admin.py

    - PART 2: Customising the admin site
        - extending the FT
        - add a second model: Choice
        - more detailed unit tests

    - PART 3: the site home page
        - the Django Test Client
        - views.py
        - templates

    - PART 4: individual poll voting page
        - more advanced urls 
        - forms

    - PART 5: form processing
        - POST request
        - refactoring






How we will work
----------------

    - I will provide various bits of code to build on
        - via the git repo
    
    - We'll do the first two stages together - I code, you code
        - parts 3 and 4 will be more free-form 

    - the approach: full TDD:
       - no code before tests
       - FTs first - Selenium
       - then unit tests - unittest & Django Test Client

    - We go at the speed of the slowest person
      - Ask questions
      - when I say "does everyone get that", don't just nod!
      - my glamorous assistant will keep a track of the current source tree on
        flipchart
      - JB & I will come round from time to time and take a look




PART 1:
=======

CHECKOUT
--------

checkout the base repo::

   git clone --branch workshop https://github.com/hjwp/Test-Driven-Django-Tutorial.git
   git fetch --tags
   git checkout PART1

Now we follow ``tutorial01.rst``

Some notes:

    - in the bit where I suggest a ``wget``, you can just ``mv`` the
      ``functional_test.py`` from where I've put it in the root of the repo...

    - we'll stop at the first assert in ``test_admin.py`` and try running it

    - possible discussion over ``max_length`` and ``verbose_name`` - is this 
      like testing constants?

    - time scheduled: 1 hour

    - notes for windows users:  
      - ``https`` checkout for github
      - ``move`` not ``mv``.
      - ``django-admin.py startproject mysite`` (note extra .py)
      - ``python manage.py runserver 8001``





PART 2:
=======

Checkout next part::

    git stash
    git checkout PART2 

Now we follow ``tutorial03.rst`` 
                         ^- NB - 03, not 02 ;-)






PART 3:
=======

Checkout next part::

    git stash
    git checkout PART3 

Now we follow ``tutorial04.rst`` 

