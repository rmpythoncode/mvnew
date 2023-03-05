from django.db import models
from vendor.models import Vendor
from PIL import Image

import os
from django.conf import settings


class Category(models.Model):
  vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
  category_name = models.CharField(max_length=50)
  category_slug = models.SlugField(max_length=100, unique=True)
  description = models.CharField(max_length=250, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    ordering = ('category_name',)
    verbose_name = 'Categoria'
    verbose_name_plural = 'Categorias'

  def clean(self):
    self.name = self.category_name.capitalize()
  
  def __str__(self):
    return self.category_name
  

class SubCategory(models.Model):
  vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
  category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcatitems')
  subcategory_name = models.CharField(max_length=50)
  subcategory_slug = models.SlugField(max_length=100, unique=True)
  description = models.CharField(max_length=250, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    ordering = ('subcategory_name',)
    verbose_name = 'SubCategoria'
    verbose_name_plural = 'SubCategorias'

  def clean(self):
    self.name = self.subcategory_name.capitalize()
  
  def __str__(self):
    return self.subcategory_name


class Product(models.Model):
  vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
  category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='productitems')
  subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
  product_name = models.CharField(max_length=50)
  product_slug = models.SlugField(max_length=100, unique=True)
  description = models.TextField(max_length=250, blank=True)
  price = models.DecimalField(max_digits=10, decimal_places=2)
  sale_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
  image = models.ImageField(upload_to='productimage')
  is_available = models.BooleanField(default=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)


  class Meta:
    ordering = ('product_name',)
    verbose_name = 'Produto'
    verbose_name_plural = 'Produtos'



  def save(self, *args, **kwargs):
    super().save(*args, **kwargs)

    if self.image:
      img = Image.open(self.image.path)

      # if img.width > 100 or img.height > 100:
      #   new_width = 100
      #   new_height = int(new_width / img.width * img.width)
      #   img = img.resize((new_height, new_width))
      #   img.save(self.image.path)


      if img.height > 100 or img.width > 100:
        new_height = 200
        new_width = int(new_height / img.height * img.width)
        img = img.resize((new_width, new_height))
        img.save(self.image.path)


  def __str__(self):
    return self.product_name
