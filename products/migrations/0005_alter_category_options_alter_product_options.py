# Generated by Django 4.1.6 on 2023-02-04 16:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_subcategory'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('category_name',), 'verbose_name': 'Categoria', 'verbose_name_plural': 'Categorias'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('product_name',), 'verbose_name': 'Produto', 'verbose_name_plural': 'Produtos'},
        ),
    ]
