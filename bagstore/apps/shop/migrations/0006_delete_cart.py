# Generated by Django 5.0.6 on 2024-07-01 10:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_alter_evaluation_unique_together'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Cart',
        ),
    ]
