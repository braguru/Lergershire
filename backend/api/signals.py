from django.db.models.signals import post_save, post_delete
from .models import User, Profile
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    # If the user is created, create a new profile object
    if created:
        user = instance
        profile = Profile.objects.create(user=user, username=user.username, 
                               phone_number=user.phone_number, email=user.email, 
                               investment_objectives=user.investment_objectives)
        
        
        
@receiver(post_save, sender=Profile)        
def update_profile(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    if created == False:
        user.username = profile.username
        user.phone_number = profile.phone_number
        user.email = profile.email
        user.investment_objectives = profile.investment_objectives
        user.save()
        
        
        
@receiver(post_delete, sender=Profile)
def delete_profile(sender, instance, **kwargs):
    user = instance.user
    user.delete()
