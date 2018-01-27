import datetime

from django.db import models

from django.utils.translation import ugettext_lazy as _

# Create your models here.


class Announcement(models.Model):

    title = models.CharField(max_length=150)
    content = models.TextField()
    date = models.DateField(_("Date"), default=datetime.date.today)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title