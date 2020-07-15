from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
import json
from .models import Groups, GroupChats, GroupUsers, ImageUploadGroup
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from itertools import chain

import re
# Create your views here.
@login_required
def GroupCreate(request, groupname):
    x = re.findall("[A-Za-z0-9]", groupname)
    p = ''
    x = p.join(x)  
    grouplist = request.user.creator.filter(groupname = x)
    if(len(grouplist) == 0):
        participants = request.session['groupParticipants']
        a = Groups.objects.create(admin = request.user, groupname = x, num = len(participants), participants = str(participants))
        for user in participants:
            GroupUsers.objects.create(group = a, user = User.objects.get(username = user))
        return render(request, 'groups/groupview.html', {'groupname' : x, 'user' : request.user.username, 'chats' : [] ,'len' : 0})
    else:
        return HttpResponse("Already exists")
def GroupView(request, groupname):
    x = re.findall("[A-Za-z0-9]", groupname)
    p = ''
    x = p.join(x)  
    group = Groups.objects.get(groupname = x)
    if request.method == 'POST':
        try:
            print(request.FILES)
            myfile = request.FILES['data']
            fr = FileSystemStorage()
            filename = fr.save(myfile.name, myfile)
            url = fr.url(filename)
            print()
            ImageUploadGroup.objects.create(path_image = url, filename = filename, chatconnect = group, sender = request.user)
            print('Imageuploaded')
            return JsonResponse({'error': False, 'path': url})
        except:
            return JsonResponse({'error': True})
    chats = group.chats.all()
    images = group.sentimages.all()
    total_msgs = list(chain(chats, images))
    total_msgs = sorted(total_msgs, key=lambda obj: obj.time)
    return render(request, 'groups/groupview.html', {'groupname' : x, 'user' : request.user.username, 'chats' : total_msgs, 'len' : len(total_msgs)})
    
