from django.db.models.signals import post_save, pre_save, post_init
from django.dispatch import receiver
from .models import User, UserProfile

# import os
# from django.conf import settings

@receiver(post_save, sender=User)
def post_save_create_profile_receiver(sender, instance, created, **kwargs):
  if created:
    UserProfile.objects.create(user=instance)
  else:
    try:
      profile = UserProfile.objects.get(user=instance)
      profile.save()
    except:
      # Create the userprofile if not exist
      UserProfile.objects.create(user=instance)


@receiver(pre_save, sender=User)
def pre_save_profile_receiver(sender, instance, **kwargs):
  pass
# post_save.connect(post_save_create_profile_receiver, sender=User)







# @receiver(pre_save, sender=UserProfile)
# def delete_old_file_cover_photo(sender, instance, **kwargs):
#   # on creation, signal callback won't be triggered 
#   if instance._state.adding and not instance.pk:
#     return False
  
#   try:
#     old_file = sender.objects.get(pk=instance.pk).cover_photo
#   except sender.DoesNotExist:
#     return False
  
#   # comparing the new file with the old one
#   image = instance.cover_photo
#   if not old_file == image:
#     if os.path.isfile(old_file.path):
#       os.remove(old_file.path)


# @receiver(pre_save, sender=UserProfile)
# def delete_old_file_profile_picture(sender, instance, **kwargs):
#   # on creation, signal callback won't be triggered 
#   if instance._state.adding and not instance.pk:
#     return False
  
#   try:
#     old_file = sender.objects.get(pk=instance.pk).profile_picture
#   except sender.DoesNotExist:
#     return False
  
#   # comparing the new file with the old one
#   image = instance.profile_picture
#   if not old_file == image:
#     if os.path.isfile(old_file.path):
#       os.remove(old_file.path)