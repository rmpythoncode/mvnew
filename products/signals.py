from django.db.models.signals import pre_save
import os
from django.dispatch import receiver
from .models import Product


@receiver(pre_save, sender=Product)
def delete_old_file(sender, instance, **kwargs):
  # on creation, signal callback won't be triggered 
  if instance._state.adding and not instance.pk:
    return False
  
  try:
    old_file = sender.objects.get(pk=instance.pk).image
  except sender.DoesNotExist:
    return False
  
  # comparing the new file with the old one
  image = instance.image
  if not old_file == image:
    if os.path.isfile(old_file.path):
      os.remove(old_file.path)