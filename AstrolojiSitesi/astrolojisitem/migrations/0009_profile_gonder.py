# Generated by Django 4.1.7 on 2023-04-17 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('astrolojisitem', '0008_remove_profile_birth_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='gonder',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
