from django.db import models
from django.contrib.auth.models import User

class Friends(models.Model):
    owner = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'firstfriend')
    friend = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'secondfriend')

    class Meta:
        verbose_name_plural = 'Friends'

class PersonalChats(models.Model):
    friend = models.ForeignKey(Friends, on_delete = models.CASCADE, related_name='friends')
    chat = models.TextField(default='-')
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'PersonalChats'

