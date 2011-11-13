from django import forms

class PollVoteForm(forms.Form):
    vote = forms.ChoiceField()

    def __init__(self, poll):
        super(self.__class__, self).__init__()
        self.fields['vote'].choices = [c.choice for c in poll.choice_set.all()]

'''
class PollVoteForm2(Form):
    vote = ChoiceField(widget=RadioSelect())
    def __init__(self, poll):
        super(self.__class__, self).__init__()
        self.poll = poll
        self.fields['vote'].choices = [c.choice for c in poll.choice_set.all()]

'''



