from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager
# Create your models here.

GENDER_CHOISES=[
    ('M','Male'),
    ('F','Female'),
]
BLOOD_CHOISES=[
    ('A+','A+'),
    ('A-','A-'),
    ('B+','B+'),
    ('B-','B-'),
    ('O+','O+'),
    ('O-','O-'),

]

IDENTITY_CHOISES=[
    ('Passport ID','Passport ID'),
    ('National ID','National'),
]


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self,email,password,**kwargs):
        if not email:
            raise ValueError("User must have an email address")
        if not password:
            raise ValueError("User must have an password address")
        user = self.model(email=email,**kwargs)
        user.set_password(password)
        user.save()
        return user


    def create_superuser(self,email,password,**kwargs):
        kwargs.setdefault('is_staff',True)
        kwargs.setdefault('is_superuser',True)

        if kwargs.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email,password,**kwargs)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255,unique=True)
    first_name = models.CharField(max_length=255,blank=True,null=True)
    last_name = models.CharField(max_length=255,blank=True,null=True)
    date_of_birth = models.DateField(null=True,blank=True,help_text="Please enter a date format: YYYY-MM-DD")
    gender = models.CharField(max_length=255,blank=True,null=True,choices=GENDER_CHOISES)
    blood_groups = models.CharField(max_length=255,blank=True,null=True,choices=BLOOD_CHOISES)
    identity_document_type = models.CharField(max_length=255,blank=True,null=True,choices=IDENTITY_CHOISES)
    identity_document_number = models.CharField(max_length=255,blank=True,null=True)
    photo = models.ImageField(null=True,blank=True,upload_to='profilephoto')
    date_joine = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(auto_now=True)
    is_email_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']
    
    objects = UserManager()



    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'