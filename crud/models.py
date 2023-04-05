from django.db import models

# Create your models here.
# importing abstract user for mild modifications 
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    
    # defining the fields 
    
    id = models.BigAutoField(primary_key=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    phone_number = models.BigIntegerField(null=True , blank=True) 
    country_code = models.CharField(max_length=10, blank=True, null=True)
    phone_verified = models.DateTimeField(blank=True,null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True )
    last_name = models.CharField(max_length=255, blank=True, null=True)
    profile_pic = models.ImageField(default='default.jpg', upload_to='profile_pics',blank=True, null=True)
    last_login_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    deleted_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True,null=True)
    updated_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    
    # replacing the unique identifier from username to email 
    
    REQUIRED_FIELDS = ['username']
    
    USERNAME_FIELD = 'email'
    
    

class profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE) # one user can only have 1 profile pic 
    profile_picture = models.ImageField(default = 'default.jpg', upload_to = 'profile_pics') 

    
    def __str__(self):
        return f'{self.user.username} Profile'
    
    
    
