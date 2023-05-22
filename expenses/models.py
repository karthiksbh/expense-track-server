from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
    
class CustomUserManager(BaseUserManager):

    def create_superuser(self, email, first_name, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'is_staff must be True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'is_superuser must be true')
        return self.create_user(email, first_name, password, **other_fields)

    def create_user(self, email, first_name, password, **other_fields):

        if not email:
            raise ValueError(_('Email ID is required for creating the user'))

        email = self.normalize_email(email)
        user = self.model(email=email,
                          first_name=first_name, **other_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('Email Address'), unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150, null=True,blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    def __str__(self):
        return str(self.email)

TYPE_CHOICES = (
    ('Income','Income'),
    ('Expenditure','Expenditure')
)

class Expenses(models.Model):
    user_ref = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    amount = models.FloatField()
    typeof = models.CharField(choices=TYPE_CHOICES,max_length=255)
    createdOn = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.id)
