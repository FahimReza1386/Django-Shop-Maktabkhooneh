from django.db import models
from django.contrib.auth.models import (AbstractBaseUser ,BaseUserManager,PermissionsMixin)
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver
from django.core.exceptions import ValidationError 
from .validators import validate_iranian_phone_number
from django.dispatch import receiver
from django.db.models.signals import post_save  
import re  


# Create your models here.


class UserType(models.IntegerChoices):
    customer = 1 , _("Customer")
    admin = 2 , _("Admin")
    superuser = 3 , _("SuperUser")

class UserManager(BaseUserManager):

    """
        THe Create User and SuperUser
    """

    def create_user(self , email , password , **extra_fields):
        """
            Create and Save a User With The Given email and password , or extra data. 
        """
        if not email:
            raise ValueError(_('The Email Must Be Set'))
        email= self.normalize_email(email)
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self , email , password,**extra_fields):
        """
            Create and Save a SuperUser With The Given email and password , or extra data. 
        """
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_verified',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('type', UserType.superuser.value)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_("is_staff must have is True"))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_("is_superuser must have is True"))

        return self.create_user(email , password , **extra_fields)
    
class User(AbstractBaseUser,PermissionsMixin):

    """
        Custom User Model our App
    """

    email=models.EmailField(max_length=200 , unique=True)
    is_staff=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    is_superuser=models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date_date = models.DateTimeField(auto_now=True)
    type = models.IntegerField(choices=UserType.choices , default=UserType.customer.value)
    
    first_name=models.CharField(max_length=200)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS=[]
    objects=UserManager()

    def __str__(self):
        return self.email


class Gender(models.IntegerChoices):
    male = 1 , _("male")
    female = 2 , _("female")
    other = 3 , _("other")


class Profile(models.Model):
    user = models.OneToOneField("User", on_delete=models.CASCADE, related_name="user_profile")
    first_name = models.CharField(max_length=22)
    last_name = models.CharField(max_length=22)
    phone_number = models.CharField(max_length=12, validators=[validate_iranian_phone_number])
    gender = models.IntegerField(choices=Gender.choices, default=Gender.other.value)
    image = models.ImageField(upload_to="profile/", default='profile/default.jpg')
  
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)


    def get_fullname(self):
        if self.first_name or self.last_name:
            return f"{self.first_name} {self.last_name}"
        else:
            return f"کاربر جدید - {self.id}"

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:  
        Profile.objects.create(user=instance, pk=instance.pk)
