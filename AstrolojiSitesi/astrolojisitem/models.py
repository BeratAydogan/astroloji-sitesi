from django.db import models
from datetime import date,timedelta
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Burclar(models.Model):
    burc_adi = models.CharField(max_length=50,null=True,blank=True)
    aciklama = models.TextField(null=True,blank=True)
    aciklama_olumlu = models.TextField(null=True,blank=True)
    aciklama_olumsuz = models.TextField(null=True,blank=True)
    aciklama_guclu = models.TextField(null=True,blank=True)
    aciklama_zayif = models.TextField(null=True,blank=True)
    resim = models.ImageField(upload_to="burc_simge",null=True,blank=True)
    takimyildiz_adi = models.CharField(max_length=100,null=True,blank=True)
    takimyildiz_resim = models.ImageField(upload_to="takim_yildiz",null=True,blank=True)
    gezegeni = models.CharField(max_length=100,null=True,blank=True)
    elementi = models.CharField(max_length=100,null=True,blank=True)
    tarih = models.CharField(max_length=100,null=True,blank=True)
    niteligi = models.CharField(max_length=100, null=True,blank=True)
    mantra = models.CharField(max_length=100, null=True,blank=True)
    renk = models.CharField(max_length=100, null=True,blank=True)
    gunluk_yorum = models.TextField(null=True,blank=True)
    yukselen = models.TextField(null=True,blank=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gun = models.IntegerField(null=True,blank=True)
    ay = models.IntegerField(null=True,blank=True)
    yil = models.IntegerField(null=True,blank=True)
    gonder = models.BooleanField(null=True,blank=True,default=True)

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()






class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Topic(models.Model):
    subject = models.CharField(max_length=255)
    description = models.TextField(null=True,blank=True)
    last_updated = models.DateTimeField(auto_now_add=True)
    starter = models.ForeignKey(User, related_name='topics', on_delete=models.CASCADE)
    topic_likes = models.ManyToManyField(User, related_name='topic_likes')

    def __str__(self):
        return self.subject


class Post(models.Model):
    message = models.TextField(max_length=4000)
    topic = models.ForeignKey(Topic, related_name='posts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    post_likes = models.ManyToManyField(User, related_name='post_likes')

    def __str__(self):
        return self.message