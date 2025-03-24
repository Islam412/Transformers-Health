from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.utils.translation import gettext_lazy as _


import uuid
from shortuuid.django_fields import ShortUUIDField


# Create your models here.


def user_directory_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = "%s_%s" % (instance.id, ext)
    return "user_{0}/{1}".format(instance.user.id, filename)



class User(AbstractUser):
    frist_name = models.CharField(_('Frist Name'), max_length=255)
    last_name = models.CharField(_('Last Name'), max_length=255)
    username = models.CharField(_('Username'), max_length=255)
    email = models.EmailField(_('Email'), unique=True)
    phone = models.CharField(_("Phone Number"),max_length=50, null=True, blank=True)
    company = models.CharField(_('Company'), max_length=255, null=True, blank=True)
    date_of_birth = models.DateTimeField(_('Date Of Birth'), auto_now_add=False, blank=True, null=True)
    is_staff = models.BooleanField(_('Is Staff'), default=False)
    is_superuser = models.BooleanField(_('Super User'), default=False)


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return str(self.username)
