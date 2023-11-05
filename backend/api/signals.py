from django.db.models.signals import post_save
from .models import User, Setting
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Setting.objects.create(user=instance)
        
        
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.setting.save()