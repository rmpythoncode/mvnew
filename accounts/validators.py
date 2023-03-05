from django.core.exceptions import ValidationError
import os


def allow_only_images_validator(value):
  ext = os.path.splitext(value.name)[1]
  print(ext)
  valid_extentions = ['.jpg', '.jpeg', '.png']
  if not ext.lower() in valid_extentions:
    raise ValidationError('Tipo de arquivo não suportado. Os arquivos suportados são: '+str(valid_extentions))