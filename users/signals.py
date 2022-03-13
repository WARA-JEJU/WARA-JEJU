from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile


# User -> sender and post_save is a signal, when a User is saved then send this signal and this signal is recieved by the @receiver and this @receiver is this create_profile function that takes all of this arguments.
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:  # if the user is created then create profile object  with user = instance, of user the user that was created.
        Profile.objects.create(user=instance)

# **kwargs -> it accepts any additional keyword arguments


@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    instance.profile.save()
