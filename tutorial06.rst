
Part 6 - The Book!
==================

Thanks so much for following on this far! I'm afraid that's all there is for
now, but I am about to start on the next stage -- a proper book on TDD for 
web apps.

If you've found the tutorial useful so far, I wonder whether I can solicit 
some feeback regarding a book version?

Here's the chapter outline I've got so far.  Now, remember, this is a very rough draft, 
and it's very much bound to change, but I'd love to hear your thoughts... Especially
about some quite general questions, like:

* Am I broadly covering the right sort of stuff?
* Am I right to spend plenty of time talking about JavaScript, as well as Python?
* What should I choose as my example app?  I've written the outline as if it
  were a forums app, but I'm starting to see the appeal of one of the other classic 
  examples, the "to-do list" (very simple at base, can be extended easily, opportunities
  for sharing/social bits, plenty of stuff to do on the client-side too...).  What 
  would you choose as an example?


===============================================
PART 1 - Beginning web app development with TDD
===============================================

The idea is to dive straight in with a practical example, rather than talking
a lot of theory up-front.   I had originally thought to start with a toy example
(cf these 3 abandoned chapters: http://www.tdd-django-tutorial.com/tutorial/6/ ), 
but I decided that people prefer real practical stuff to toy examples...

I also want the first few chapters to be very short + bit-sized, so that the
reader feels like they're really making progress quickly... (the inspiration
comes from Kent Beck's TDD by Example, an awesome book)

Essentially part 1 is a re-hash of this online tutorial, using a differnt example
app...


1: Our first functional test with Selenium
------------------------------------------


* Briefly discuss difference between functional testing (AKA acceptance
  testing, integration testing, whatever) and unit testing
* Write first test - Introduce Selenium, `setUp`, `tearDown`
* Demonstrate we can get it to open a web browser, and navigate to a web page
  eg - google.com


2: Getting Django set-up and running
------------------------------------

* Change our test to look for the test server
* Switch to Django LiveServerTestCase. Explain
* Get the first test running and failing for a sensible reason
* Create django project `django-admin.py startproject`
* It worked!



3: A static front page
----------------------

* Look for "Welcome to the Forums", or similar
* `urls.py`, `direct_to_template` ?



4: Super-users and the Django admin site
----------------------------------------

* Extend FT to try and log in
* Explain the admin site
* Database setup, `settings.py`, `syncdb`, `admin.py`
* `runserver` to show login code
* Explain difference between test database and real database
* Fixtures



5: First unit tests and Database model 
--------------------------------------

* Distinction between unit tests and functional tests
* Extend FT to try and create a new topic
* new app
* `models.py`
* test/code cycle



6: Testing a view
-----------------

* urls.py again
* Test view as a function
* assert on string contents


7: Django's template system
----------------------------

* Introduce template syntax
* Keep testing as a function
* The, introduce the Django Test Client



8: Reflections: what to test, what not to test
-----------------------------------------------

* time for a bit of theory/philosophy
* "Don't test constants"
* Test logic
* Tests for simple stuff should be simple, so not much effort


9: Simple Forms
----------------

* Manually coded HTML
* Refactor test classes


10: User Authentication
-----------------------

* Sign up, login/logout
* Email?


11: More advanced forms
-----------------------

* Use Django Forms classes



12: On Refactoring
------------------

* Martin Fowler
* Tests critical
* Methodical process - explain step by step



13: Pagination
--------------

* Extend various old unit tests and FTs



======================================================
PART 2: More advanced testing for a more advanced site
======================================================

14: Notifications
------------------------------

* Django Notifications, for post edits


15: Adding style with MarkDown
------------------------------

* Using an external library


16: Switching to OAuth: Mocking
-------------------------------

* "Don't store passwords"
* Discuss challenges of external dependencies


17: Getting Dynamic: Testing Javascript part 1
----------------------------------------------

* Simple input validation
* Choose JS unit testing framework (probably Qunit, or YUI)



18: Testing Javascript part 2 - Ajax
------------------------------------

* Dynamic previews of post input


19: Getting pretty: Bootstrap
-----------------------------

* Bring in nicer UI elements


20: Getting pretty: Gravatar
----------------------------

* pictures for users



==============================
PART 3: Getting seriously sexy
==============================

21: Getting serious about the client-side + single-page website?
----------------------------------------------------------------

* Introduce one of the client-side js frameworks -- backbone.js / ember.js / angular


22: Switching Databases 1: PostgreSQL
----------------------------------------------

* show how Django makes this easy



23: Websockets and Async on the server-side
-------------------------------------------

* we want dynamic notifications of when new posts appear on a thread we're
  looking at
* Need to spin up, Tornado/Twisted/Gevent as well as Django LiveServerTestCase
* FT opens multiple browser tabs in parallel
* Big change!


24: Switching Databases 2: NoSQL and MongoDB
----------------------------------------------

* obligatory discussion of NoSQL and MongoDB
* descrine installation, particularities of testing


26: Continuous Integration 
--------------------------

* Need to build 3 server types
* Jenkins (or maybe buildbot)
* Need to adapt Fts, maybe rely less on LiveServerTestCase



27: Caching for screamingly fast performance
--------------------------------------------

* unit testing `memcached`
* Functionally testing performance
* Apache `ab` testing




Well, that's what I have so far.  What do you think?  Have I missed anything
out?  Does anything seem superfluous?  Most importantly, would you buy it?  

