from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator 
from django.utils import timezone

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True)
    profile_pic = models.ImageField(default='default.jpg', upload_to='profile_pictures')
    website_url = models.CharField(max_length=255, null=True, blank=True)
    facebook_url = models.CharField(max_length=255, null=True, blank=True)
    twitter_url = models.CharField(max_length=255, null=True, blank=True)
    instagram_url = models.CharField(max_length=255, null=True, blank=True)
    pinterest_url = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        #return str(self.user)
        return f'{self.user.username} Profile'

    def get_absolute_url(self):
        return reverse('home')

    
class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='receiver', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


class Presentations(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    main_title = models.TextField() #first slide title
    titles = models.TextField() #Titles of other slides added together 
    date_created = models.DateTimeField(default=timezone.now)
    #0 meaning presentation is not shared, 1 presentation is shared. defaults to 0
    is_shared = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(1)])
    presentation = models.CharField(max_length=210) 