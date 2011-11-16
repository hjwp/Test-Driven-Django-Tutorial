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


The Plan
--------

    - to run through contents of Django tutorial

    - ie, a polls/voting app

    - I will provide various materials
      - via  a git repo

    - PART 1: the Django admin site
        - first selenium FT
        - first unit tests
        - models.py

    - PART 2: the site home page
        - the Django Test Client
        - views.py
        - templates

    - PART 3: individual poll voting pagekk
        - more advanced url capturing
        - forms

    - PART 4: (if time) - form processing


How we will work
----------------

    - We'll do the first two stages together - I code, you code
        - parts 3 and 4 will be free-form (with help!)

    - the approach: full TDD:
       - no code before tests
       - fts first - Selenium
       - then unit tests - unittest & Django Test Client








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

