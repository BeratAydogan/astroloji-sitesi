# Generated by Django 4.1.7 on 2023-04-16 13:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('astrolojisitem', '0007_profile_ay_profile_gun_profile_yil'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='birth_date',
        ),
    ]
