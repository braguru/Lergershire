from django.db.models.signals import post_save
from .models import User, Profile
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    # If the user is created, create a new Setting object
    if created:
        Profile.objects.create(user=instance)
    else:
        # If the user is being updated, update the associated Setting object
        try:
            profile = Profile.objects.get(user=instance)
            # You can update fields of the setting if needed
            profile.save()
        except Profile.DoesNotExist:
            # If the Setting object doesn't exist, create a new one
            Profile.objects.create(user=instance)
        
        
# @receiver(post_save, sender=User)
# def save_profile(sender, instance, created, **kwargs):
#     if created:
#         instance.setting.save()