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



ACCOUNT_STATUS = (
    ("active", "Active"),
    ("pending", "Pending"),
    ("in-active", "In-active")
)

class Account(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    user =  models.OneToOneField(User, on_delete=models.CASCADE)
    account_number = ShortUUIDField(unique=True,length=10, max_length=25, prefix="217", alphabet="1234567890")
    account_id = ShortUUIDField(unique=True,length=7, max_length=25, prefix="DEX", alphabet="1234567890")
    pin_number = ShortUUIDField(unique=True,length=4, max_length=7, alphabet="1234567890") #2737
    red_code = ShortUUIDField(unique=True,length=10, max_length=20, alphabet="abcdefgh1234567890")
    account_status = models.CharField(max_length=100, choices=ACCOUNT_STATUS, default="in-active")
    date = models.DateTimeField(auto_now_add=True)
    kyc_submitted = models.BooleanField(default=False)
    kyc_confirmed = models.BooleanField(default=False)
    recommended_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True, related_name="recommended_by")
    review = models.CharField(max_length=100, null=True, blank=True, default="Review")

    
    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.user}"



def create_account(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)

def save_account(sender, instance,**kwargs):
    instance.account.save()

post_save.connect(create_account, sender=User)
post_save.connect(save_account, sender=User)



class KYC(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    user =  models.OneToOneField(User, on_delete=models.CASCADE)
    account =  models.OneToOneField(Account, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to="kyc", default="default.jpg")
    date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user}"    

    
    class Meta:
        ordering = ['-date']
