# Generated by Django 4.1.7 on 2023-05-13 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('astrolojisitem', '0019_topic_topic_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='post_resim',
            field=models.ImageField(blank=True, null=True, upload_to='forum'),
        ),
        migrations.AddField(
            model_name='topic',
            name='topic_resim',
            field=models.ImageField(blank=True, null=True, upload_to='forum'),
        ),
    ]
