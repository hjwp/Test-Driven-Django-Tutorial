WELCOME TO THE TEST-DRIVEN-DJANGO WORKSHOP
==========================================

Required installations
----------------------

**Check your handout, Part 0, for info on the pre-reqs, and how to check
they're all installed correctly**

 - Python 2.7 
 - Git
 - Firefox
 - pip (Google "Python pip")
 - Django (``pip install django``)  -- must be >= 1.4
 - Selenium (``pip install --upgrade selenium``) -- must be absolute latest
   version.

Checkout
--------

checkout the base repo::

   git clone https://github.com/hjwp/Test-Driven-Django-Tutorial tddworkshop
   cd tddworkshop
   git checkout pycon_2013





Introduction
============

Who I am, and why should you listen to me?
------------------------------------------

    - recent convert, PythonAnywhere, etc


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
    - Windows users: use *Git Bash* as your terminal





The Plan
--------

    - To run through contents of official Django tutorial
        - ie, a polls/voting app
        - but TDD all the way

    - PART I: Django setup and a basic home page
        - first selenium FT
        - first unit tests
        - views.py, urls.py
        - templates

    - PART II: Polls, listing them, and the admin site
        - admin.py
        - models.py
        - templates

    - PART III: (if time)
        - deal with a POST request







        



How we will work
----------------

    - I code, you code
      - handouts are there for you to copy from
      - at first -- avoid copy + paste

    - I will provide various bits of code to build on
        - via the git repo
    
    - The approach: full TDD:
       - no code before tests
       - FTs first - Selenium
       - then unit tests - unittest & Django Test Client

    - We go at the speed of the slowest person
      - Ask questions
      - When I say "does everyone get that", don't just nod!
      - JB & I will come round from time to time and take a look

    - Pair programming





Some things to remember
-----------------------

* Am teaching a Discipline -- it's very rigorous TDD.  Once you've
  mastered the rules, you're free to break them

* You'll see a lot of tests failing -- don't be depressed!  An
  "expected failure" is a good thing







notes on individual parts could follow...

