# Generated by Django 5.0.6 on 2024-07-01 09:42

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_evaluation'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='evaluation',
            unique_together={('user', 'product')},
        ),
    ]