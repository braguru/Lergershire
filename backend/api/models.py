from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, AbstractUser
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail, EmailMessage
# Create your models here.

# Overide default user model

# class UserManager(BaseUserManager):
#     def create_user(self, username, email, phone_number, fund_type, amount_to_invest, investment_objectives, password=None):
        
#         if username is None:
#             raise TypeError('users should have a username')
        
#         if email is None:
#             raise TypeError('users should have a email')
        
#         user = self.model(username=username , email = self.normalize_email(email), phone_number=phone_number, fund_type=fund_type,
#                           amount_to_invest=amount_to_invest, investment_objectives=investment_objectives)
#         user.set_password(password)
#         user.save()    
        
#         return user
        
#     def create_superuser(self, username, email, password=None):
        
#         if password is None:
#             raise TypeError('A password is required')
#         if not password:
#             raise ValueError("User must have a password")
        
#         user = self.model(self, email=self.normalize_email(email))
#         user.username = username
#         user.set_password(password)
#         user.is_superuser = True
#         user.is_staff = True
#         user.save()
        
        # return user
     
class User(AbstractUser):
    FUND_TYPE = [
        ('CI', 'Citadel Fund'),
        ('CA', 'Capernaum Fund'),
        ('SM', 'Selby Medallion Fund'),
    ]
    username = models.CharField(max_length=255, unique=True, db_index=True, null=False)
    email = models.EmailField(max_length=255, unique=True, db_index=True, null=False)
    phone_number = PhoneNumberField(blank=True)
    fund_type = models.CharField(max_length=15, choices=FUND_TYPE, default='CI')
    amount_to_invest = models.IntegerField(default=0)
    investment_objectives = models.CharField(max_length=750, blank=False, default="None")
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    # objects = UserManager()
    
    
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
  
 



@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    # the below line concatenates your website's reset password URL and the reset email token which will be required at a later stage
    reset_password_url = "{}?token={}".format(
            instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm')),
            reset_password_token.key)
    email_plaintext_message = f"Open the link to reset your password: {reset_password_url}"
    """
        this below line is the django default sending email function,
        takes up some parameter (title(email title), message(email body), from(email sender), to(recipient(s))
    """
    send_mail(
        # title:
        "Password Reset for {title}".format(title="Lergershire password reset"),
        # message:
        email_plaintext_message,
        # from:
        "sabastainofori@gmail.com",
        # to:
        [reset_password_token.user.email],
        fail_silently=False
    )