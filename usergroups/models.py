from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Groups(models.Model):
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator')
    groupname = models.CharField(max_length = 20, unique=True)
    timeCreation = models.DateTimeField(auto_now_add=True)
    num = models.IntegerField(default=0)
    description = models.CharField(max_length = 50, default='-')
    participants = models.TextField(default='-')
    
    class Meta:
        verbose_name_plural = 'Groups'

    def __str__(self):
        return self.groupname

class GroupChats(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    group = models.ForeignKey(Groups, on_delete=models.CASCADE, related_name='chats')
    chats = models.TextField()
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'GroupChats'

class GroupUsers(models.Model):
    group = models.ForeignKey(Groups, on_delete=models.CASCADE, related_name = 'groupusers')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'groupenrolled')
    timeCreation = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'UserGroups'