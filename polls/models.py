import datetime

from django.db import models
from django.utils import timezone

from . import constants

class Question(models.Model):
    question_text = models.CharField(max_length=constants.QUESTION_TEXT_LENGTH)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def total_votes(self):
        votes = 0
        for choice in self.choice_set.all():
            votes += choice.votes
        return votes

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    # Changing appearance of this field in admin (for list_display)
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=constants.CHOICE_TEXT_LENGTH)
    votes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.choice_text


class AboutSection(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField(max_length=1000)
    # field for being able to order the sections in the desired order to be displayed
    display_order = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return self.title