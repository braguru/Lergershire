from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

# Overide default user model

class UserManager(BaseUserManager):
    def create_user(self, username, email, phone_number, fund_type, amount_to_invest, investment_objectives, password=None):
        
        if username is None:
            raise TypeError('users should have a username')
        
        if email is None:
            raise TypeError('users should have a email')
        
        user = self.model(username=username , email = self.normalize_email(email), phone_number=phone_number, fund_type=fund_type,
                          amount_to_invest=amount_to_invest, investment_objectives=investment_objectives)
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
    FUND_TYPE = [
        ('CI', 'Citadel Fund'),
        ('CA', 'Capernaum Fund'),
        ('SM', 'Selby Medallion Fund'),
    ]
    username = models.CharField(max_length=255, unique=True, db_index=True, null=False)
    email = models.EmailField(max_length=255, unique=True, db_index=True, null=False)
    phone_number = PhoneNumberField(blank=True, null=False)
    fund_type = models.CharField(max_length=15, choices=FUND_TYPE, default='CI')
    # profile_picture = models.ImageField(blank=True, null=True)
    amount_to_invest = models.IntegerField(default=0)
    investment_objectives = models.CharField(max_length=750, blank=True, null=True)
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
    


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    profile_pic = models.ImageField(default='default.jpg', upload_to='profile_pics')
    username = models.CharField(max_length=255, default="", null=False) 
    phone_number = PhoneNumberField(blank=True)
    email = models.EmailField(max_length=255, default="", null=False)
    investment_objectives = models.CharField(max_length=750, default="", null=False)
        

    def __str__(self):
        return f'{self.user.username} Profile'
  
 