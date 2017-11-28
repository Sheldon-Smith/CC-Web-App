from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import User

from django.db import models

from django.db.models.signals import post_save

from django.dispatch import receiver

from account.choices import CLASS_CHOICES


class UserManager(BaseUserManager):

    def _create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError('The email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


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

