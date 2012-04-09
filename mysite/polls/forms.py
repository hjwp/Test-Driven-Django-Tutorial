from django import forms

class PollVoteForm(forms.Form):
    vote = forms.ChoiceField(widget=forms.RadioSelect())

    def __init__(self, poll):
        forms.Form.__init__(self)
        self.fields['vote'].choices = [(c.id, c.choice) for c in poll.choice_set.all()]
