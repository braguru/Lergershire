from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

# Overide default user model

class UserManager(BaseUserManager):
    def create_user(self, username, email, phone_number, password=None):
        
        if username is None:
            raise TypeError('users should have a username')
        
        if email is None:
            raise TypeError('users should have a email')
        
        user = self.model(username=username , email = self.normalize_email(email), phone_number=phone_number)
        user.set_password(password)
        user.save()    
        
        return user
        
    def create_superuser(self, username, email, password=None):
        
        if password is None:
            raise TypeError('A password is required')
        
        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        
        return user
     
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True, db_index=True)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    phone_number = PhoneNumberField(blank=True)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    objects = UserManager()
    
    
    def __str__(self):
        return self.username
    
    
    
 ## End of overiding user model ###   
 

class InvitationEmail(models.Model):
    # Email field
    email = models.EmailField(unique=True)  # 'unique=True' enforces uniqueness
    sent_at = models.DateTimeField(default=timezone.now)

    # Additional fields and methods for your model

    def __str__(self):
        return self.email  # Return the email when the object is converted to a string
    

class login(models.Model):
    uname = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=254)
    
    def __str__(self):
        return self.uname

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    profile_pic = models.ImageField(default='default.jpg', upload_to='profile_pics')
    Investment_objectives = models.CharField(max_length=500)
        

    def __str__(self):
        return f'{self.user.username} Profile'
  
    
    
class Notification(models.Model):
    notification = models.TextField(max_length=1000)
    
    def __str__(self):
        return self.notification