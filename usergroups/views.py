from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
import json
from .models import Groups, GroupChats, GroupUsers
from django.contrib.auth.models import User
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
    print(x, 'groupname')
    group = Groups.objects.get(groupname = x)
    print(group, 'group')
    chats = group.chats.all()
    print('-----------------------------------')
    print(chats)
    print('-----------------------------------')
    return render(request, 'groups/groupview.html', {'groupname' : x, 'user' : request.user.username, 'chats' : chats, 'len' : len(chats)})
    
