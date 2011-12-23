Welcome to part 5 - this week we'll be looking at processing user
input from forms.

Tutorial 5: Processing form submissions
=======================================

Here's the outline of what we're going to do in this tutorial:

    * handle POST requests

    * tbc!


Finishing the FT
----------------

Let's pick up from the ``TODO`` in our FT, and extend it to include viewing the
effects of submitting a vote on a poll. In ``fts/test_polls.py``:

.. sourcecode:: python

        [...] 

        # Herbert clicks 'submit'
        self.browser.find_element_by_css_selector(
                "input[type='submit']"
            ).click()

        # The page refreshes, and he sees that his choice
        # has updated the results.  they now say
        # "100 %: very awesome".
        self.fail('TODO')

        # The page also says "1 votes"

        # Satisfied, he goes back to sleep

