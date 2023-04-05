from django.db.models.signals import post_save
from crud.models import User
from django.dispatch import receiver
from .models import profile


@receiver(post_save,sender=User)  # create profile function is the receiver that gets post_save and User(sender) as attributes
def create_profile(sender,instance,created,**kwargs):
    if created:
        profile.objects.create(user=instance) # creates user instance 
        
        

@receiver(post_save,sender=User) 
def save_profile(sender,instance,**kwargs):
    instance.profile.save()