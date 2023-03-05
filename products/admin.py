from django.contrib import admin
from .models import SubCategory, Category, Product


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'category_slug': ('category_name',)}
    list_display = ('category_name', 'pk', 'vendor', 'updated_at')
    search_fields = ('category_name', 'vendor__vendor_name')


class SubCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'subcategory_slug': ('subcategory_name',)}
    list_display = ('subcategory_name', 'vendor', 'updated_at')
    search_fields = ('subcategory_name', 'vendor__vendor_name')


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'product_slug': ('product_name',)}
    list_display = ('product_name', 'category', 'vendor', 'price', 'is_available', 'updated_at')
    search_fields = ('product_name', 'category__category_name', 'vendor__vendor_name', 'price')
    list_filter = ('is_available',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Product, ProductAdmin)