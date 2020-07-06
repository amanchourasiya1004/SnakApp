from django.db import models

# Create your models here.
class Users(models.Model):
    username = models.CharField(unique=True, max_length = 20)
    password = models.CharField(max_length = 20)
    email = models.EmailField(max_length = 20)
