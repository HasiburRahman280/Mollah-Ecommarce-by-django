from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class Profile(models.Model):
    CHOICE_GENDER = (
        ('male','male'),
        ('female','female')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile',null=True)
    full_name = models.CharField(max_length=50,blank=True,null=True)
    email = models.EmailField(blank=True,null=True)
    phone = models.CharField(max_length=50,blank=True,null=True)
    address = models.CharField(max_length=200,blank=True,null=True)
    gender = models.CharField(max_length=6,choices=CHOICE_GENDER)
    create = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}'

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

class ProfilePicture(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='pro_pics')
    image= models.ImageField(upload_to='profile_images')




