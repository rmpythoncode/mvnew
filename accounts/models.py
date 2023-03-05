from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.gis.db import models as gismodels
from django.contrib.gis.geos import Point
from PIL import Image

# Create your models here.

class UserManager(BaseUserManager):
  def create_user(self, first_name, last_name, username, email, password=None):
    if not email:
      raise ValueError("Usuário deve entrar com um email válido.")
    
    if not username:
      raise ValueError("Usuário deve ter um nome de usuário.")    

    user = self.model(
      email = self.normalize_email(email),
      username = username,
      first_name = first_name,
      last_name = last_name,
    )
    user.set_password(password)
    user.save(using=self._db)
    return user
    
  
  def create_superuser(self, first_name, last_name, username, email, password=None):
    user = self.create_user(
      email = self.normalize_email(email),
      username = username,
      password = password,
      first_name = first_name,
      last_name = last_name,
    )

    user.is_admin = True
    user.is_active = True
    user.is_staff = True
    user.is_superadmin = True
    user.save(using=self._db)
    return user



class User(AbstractBaseUser):

  VENDOR = 1
  CUSTOMER = 2

  ROLE_CHOICE = (
    (VENDOR, 'Vendedor'),
    (CUSTOMER, 'Cliente'),
  )

  first_name = models.CharField(max_length=50)
  last_name = models.CharField(max_length=50)
  username = models.CharField(max_length=50, unique=True)
  email = models.EmailField(max_length=100, unique=True)
  phone_number = models.CharField(max_length=16, blank=True)
  role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE, blank=True, null=True)

  # campos obrigatórios
  date_joined = models.DateTimeField(auto_now_add=True)
  last_login = models.DateTimeField(auto_now_add=True)
  created_at = models.DateTimeField(auto_now_add=True)
  modified_date = models.DateTimeField(auto_now=True)
  is_admin = models.BooleanField(default=False)
  is_active = models.BooleanField(default=False)
  is_staff = models.BooleanField(default=False)
  is_superadmin = models.BooleanField(default=False)

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

  objects = UserManager()

  def __str__(self):
    return self.email

  def has_perm(self, perm, obj=None):
    return self.is_admin

  def has_module_perms(self, app_label):
    return True

  def full_name(self):
    return str(self.first_name + ' ' + self.last_name)

  def get_role(self):
    if self.role == 1:
      user_role = 'Vendor'
    elif self.role == 2:
      user_role = 'Customer'
    return user_role




class UserProfile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
  profile_picture = models.ImageField(upload_to='users/profile_pictures', blank=True, null=True)
  cover_photo = models.ImageField(upload_to='users/cover_photos', blank=True, null=True)
  address = models.CharField(max_length=200, blank=True, null=True)
  address_complement = models.CharField(max_length=50, blank=True, null=True)
  country = models.CharField(max_length=50, blank=True, null=True)
  city = models.CharField(max_length=50, blank=True, null=True)
  state = models.CharField(max_length=50, blank=True, null=True)
  pin_code = models.CharField(max_length=50, blank=True, null=True)
  latitude = models.CharField(max_length=20, blank=True, null=True)
  longitude = models.CharField(max_length=20, blank=True, null=True)
  location = gismodels.PointField(blank=True, null=True, srid=4326)
  created_at = models.DateTimeField(auto_now_add=True)
  modified_at = models.DateTimeField(auto_now=True)

  def full_address(self):
    return f'{self.address} - {self.address_complement}'


  def __str__(self):
    return self.user.email
  

  def save(self, *args, **kwargs):
    if self.latitude and self.longitude:
      self.location = Point(float(self.longitude), float(self.latitude))
      return super(UserProfile, self).save(*args, **kwargs)
    return super(UserProfile, self).save(*args, **kwargs)
  



  def save(self, *args, **kwargs):
    super().save(*args, **kwargs)

    if self.profile_picture:
      img = Image.open(self.profile_picture.path)

      if img.height > 200 or img.width > 200:
        new_height = 100
        new_width = int(new_height / img.height * img.width)
        img = img.resize((new_width, new_height))
        img.save(self.profile_picture.path)

  


  def save(self, *args, **kwargs):
    super().save(*args, **kwargs)

    if self.cover_photo:
      img = Image.open(self.cover_photo.path)

      if img.width > 600 or img.height > 600:
        new_width = 600
        new_height = int(new_width / img.width * img.width)
        img = img.resize((new_height, new_width))
        img.save(self.cover_photo.path)