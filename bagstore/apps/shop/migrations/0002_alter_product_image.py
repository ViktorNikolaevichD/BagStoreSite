# Generated by Django 5.0.6 on 2024-06-30 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(upload_to='shop/product_photo/%Y/%m/%d/', verbose_name='Изображение'),
        ),
    ]