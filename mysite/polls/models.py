from django.db import models

class Poll(models.Model):
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField(verbose_name='Date published')

    def __unicode__(self):
        return self.question

    def total_votes(self):
        return sum(c.votes for c in self.choice_set.all())



class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def percentage(self):
        try:
            return 100.0 * self.votes / self.poll.total_votes()
        except ZeroDivisionError:
            return 0
