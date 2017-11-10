from django.contrib.auth.models import User

from django.db import models

from django.db.models.signals import post_save

from django.dispatch import receiver

from users.choices import CLASS_CHOICES


class UserProfile(models.Model):

    FRESHMAN = 'FR'
    SOPHOMORE = 'SO'
    JUNIOR = 'JR'
    SENIOR = 'SR'
    ALUMNI = 'AL'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    grad_year = models.IntegerField(blank=False,
                                    null=True,
                                    choices=CLASS_CHOICES,
                                    default=1)
    paid_dues = models.BooleanField(default=False)
    team = models.ForeignKey('teams.Team', related_name='team', null=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

