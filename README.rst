The Concept
-----------

This idea is to provide an introduction to Test-Driven web development using
Django (and Python).  Essentially, we run through the same material as the
official Django tutorial, but instead of 'just' writing code, we write tests
first at each stage - both "functional tests", in which we actually pretend to
be a user, and drive a real web browser, as well as "unit tests", which help us
to design and piece together the individual working parts of the code.

The tutorial uses the new release of Django (1.4), and covers 95% of what's covered
in the official Django tutorial.  Suggestions, comments and feedback are gratefully
received... What should I do next??

Website:
--------

http://tdd-django-tutorial.com/



Who is this for?
----------------

Maybe you've done a bit of Python programming, and you're thinking of learning
Django, and you want to do it "properly".  Maybe you've done some test-driven
web development in another language, and you want to find out about how it all
works in the Python world.  Most importantly, you've heard of, or had experience
of, working on a project where complexity has started to get the better of you,
where you're scared to make changes, and you wished there had been better
testing from the get-go.


Who is this not for?
--------------------

If you know Python, Django and Selenium inside out, I suspect there's better things
that you can do with your time. If you're a total beginner programmer, I also
think it might not be quite right for you - you might do better to get a couple
of other tutorials under your belt first.  If you're already a programmer, but
have never tried Python, you'll be fine, but I thoroughly recommend the excellent
"Dive into Python" for a bit more of an insight into the language itself.



Why should you listen to me?
----------------------------

I was lucky enough to get my first "proper" software development job about a
year ago with a bunch of Extreme Programming fanatics, who've thoroughly
inculcated me into their cult of Test-Driven development.  Believe me when I
say I'm contrary enough to have questioned every single practice, challenged
every single decision, moaned about every extra minute spent doing "pointless"
tests instead of writing "proper" code.  But I've come round to the idea now,
and whenever I've had to go back to some of my old projects which don't have
tests, boy have I ever realised the wisdom of the approach.

So, I've learnt from some really good people, and the learning process is still 
fresh in my mind, so I hope I'll be good at communicating it.  Most importantly,
I still have the passion of a recent convert, so I hope I'll be good at conveying
some enthusiasm.



Why Test-Driven Development?
----------------------------

The thing is, when you start out on  a small project, you don't really need tests.
Tests take time to write - as much as, if not more than, the actual code for your
application.  You've got to learn testing frameworks, and they inevitably come 
with a whole host of their own problems (and this applies especially to web-browser
testing. oh boy.).  Meanwhile, you know you could just knock out a few lines of
code, and your application would be off the ground, and would start to be
useful. There are deadlines!  Clients who are paying for your time!  Or maybe
just the smell of that `Internet money`, and arriving late to the party means
none of it will be for you!

Well, that's all true.  At first.  At first, it's obvious whether everything 
works.  You can just log into the dev server, click around a bit, and see
whether everything looks OK.  And changing this bit of code over `here`, is
only ever going to affect these things `here` and `here`... So it's easy to
change stuff and see if you've broken anything...

But as soon as your project gets slightly larger, complexity rears its ugly
head.  Combinatorial explosion starts to make you its bitch. Changes start to
have unpredictable effects.  You start to worry about making changes to that
thing over there, because you wrote it ages ago, and you're pretty sure other
things depend on it... best to just use it as it is, even though it's hideously
ugly...  Well, anyway, changing this thing over `here` shouldn't affect too much
stuff.  I'll just run through the main bits of the site to check... Can't possibly
check everything though... Oh well, I'll just deploy and see if anyone complains...

Automated tests can save you from this fate.  If you have automated tests, you can
know for sure whether or not your latest changes broke anything.  With tests, 
you're free to keep refactoring your code, to keep trying out new ways to optimise
things, to keep adding new functionality, safe in the knowledge that your tests
will let you know if you get things wrong.

Look, that's got to be enough evangelising.  If you don't believe me, just ask
someone else with experience.  They know.  Now, onto the practicals.


Convinced?  Get on with part 1 of the tutorial then!

http://harry.pythonanywhere.com/tutorial/1/


USEFUL LINKS
------------

https://tdd-django-tutorial.com

https://github.com/hjwp/Test-Driven-Django-Tutorial

https://docs.djangoproject.com/en/1.4/intro/tutorial02/

http://seleniumhq.org/docs/03_webdriver.html

http://code.google.com/p/selenium/source/browse/trunk/py/selenium/webdriver/remote/webdriver.py

http://code.google.com/p/selenium/source/browse/trunk/py/selenium/webdriver/remote/webelement.py

http://www.pythonanywhere.com/
