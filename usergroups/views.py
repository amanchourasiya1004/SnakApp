from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
import json
from .models import Groups, GroupChats, GroupUsers
from django.contrib.auth.models import User
# Create your views here.
@login_required
def GroupView(request, groupname):
    
    grouplist = request.user.creator.filter(groupname = groupname)
    participants = request.session['groupParticipants']
    if(len(grouplist) == 0):
        a = Groups.objects.create(admin = request.user, groupname = groupname, num = len(participants), participants = str(participants))
        for user in participants:
            GroupUsers.objects.create(group = a, user = User.objects.get(username = user))
    return render(request, 'groups/groupview.html', {'groupname' : groupname, 'user' : request.user.username})

# Create your views here.
