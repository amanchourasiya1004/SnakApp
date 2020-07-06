from django.contrib import admin
from .models import PersonalChats, Friends
# Register your models here.

admin.site.register(PersonalChats)
admin.site.register(Friends)