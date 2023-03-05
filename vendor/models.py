from django.db import models
from accounts.models import User, UserProfile
from accounts.utils import send_notification_email

# Create your models here.

class Vendor(models.Model):
  user = models.OneToOneField(User, on_delete= models.CASCADE, related_name='user')
  user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='userprofile')
  vendor_name = models.CharField(max_length=50)
  vendor_description = models.CharField(max_length=2000)
  vendor_slug = models.SlugField(max_length=100, unique=True)
  vendor_CNPJ = models.CharField(max_length=30)
  is_approved = models.BooleanField(default=False)
  created_at = models.DateTimeField(auto_now_add=True)
  modified_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.vendor_name
  

  def save(self, *args, **kwargs):
    if self.pk is not None:
      # Update
      orig = Vendor.objects.get(pk=self.pk)
      if orig.is_approved != self.is_approved:
        mail_template = "accounts/emails/admin_aproval_email.html"
        context = {
          'user': self.user,
          'is_approved': self.is_approved,
          'to_email': self.user.email,
        }

        if self.is_approved == True:
          # Envia email de notificação
          mail_subject = "Seu negócio foi APROVADO!!!"
          send_notification_email(mail_subject, mail_template, context)

        else:
          mail_subject = "Nos desculpe. Seu negócio foi reprovado!!!"
          send_notification_email(mail_subject, mail_template, context)

    return super(Vendor, self).save(*args, **kwargs)