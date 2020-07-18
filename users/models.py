from django.db import models
from django.core.files.storage import FileSystemStorage


# Create your models here.

fr = FileSystemStorage(location = '/media/profilepic')
class Users(models.Model):
    username = models.CharField(unique=True, max_length = 20)
    password = models.CharField(max_length = 20)
    email = models.EmailField(max_length = 20)

class ProfilePic(models.Model):
    img = models.ImageField(storage = fr)
    user = models.CharField(max_length = 20, default='-')
