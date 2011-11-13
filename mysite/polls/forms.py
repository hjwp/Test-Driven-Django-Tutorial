from django import forms

class PollVoteForm(forms.Form):
    vote = forms.ChoiceField(widget=forms.RadioSelect())

    def __init__(self, poll):
        super(self.__class__, self).__init__()
        self.fields['vote'].choices = [(c.id, c.choice) for c in poll.choice_set.all()]


'''
(saving this for use later...)
from polls.models import Choice
class PollVoteForm2(Form):
    vote = forms.ModelChoiceField(queryset=[])
    def __init__(self, poll):
        super(self.__class__, self).__init__()
        self.fields['vote'].queryset = poll.choice_set.all()
'''



