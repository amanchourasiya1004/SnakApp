from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import JsonResponse
from .models import PersonalChats, Friends
from itertools import chain
import json

@login_required
def HomeView(request):
    finalchat = []
    # Group message section
    groupenrolled = request.user.groupenrolled.all()
    for i in groupenrolled:
        k = i.group.chats.latest('time')
        finalchat.append([i.group.groupname, k.chats, k.time])
    # Group message section end

    # Friends section start
    friends = list(chain(request.user.firstfriend.all(), request.user.secondfriend.all()))
    for i in friends:
        if(i.owner.username != request.user.username):
            name = i.owner.username
        else:
            name = i.friend.username
        k = i.friends.latest('time')
        finalchat.append([name, k.chat, k.time])
    # Friends section end
    sorted_chat = sorted(finalchat, key=lambda obj: obj[2], reverse=True)
    chat = []
    for i in sorted_chat:
        chat.append([i[0], i[1]])
    chats = json.dumps(chat)
    return render(request, 'main/home.html', {'chats' : chats})

@login_required
def SearchView(request):
    if(request.is_ajax() and request.method == 'GET'):
        query = request.GET.get('search', None)
        result = User.objects.filter(username__icontains = query)
        serialize_result = serializers.serialize('json', result)
        return JsonResponse({'result' : serialize_result, 'length' : len(result)}, status = 200)
    return render(request, 'main/search_single.html')


@login_required
def personalChatView(request, name):
    arr = [request.user.username, name]
    arr.sort()
    if(len(Friends.objects.filter(owner__username = arr[0], friend__username = arr[1])) == 0):
        Friends.objects.create(owner = User.objects.get(username = arr[0]), friend = User.objects.get(username = arr[1]))
        messages = []
    else:
        messages = Friends.objects.get(owner__username = arr[0], friend__username = arr[1]).friends.all()
    return render(request, 'main/personalchat.html', {'otheruser' : name, 'me' : request.user.username, 'msgs' : messages, 'length' : len(messages)})

@login_required
def CreateGroup(request):
    if(request.is_ajax() and request.method == 'GET'):
        query = request.GET.get('search', None)
        result = User.objects.filter(username__icontains = query)
        serialize_result = serializers.serialize('json', result)
        return JsonResponse({'result' : serialize_result, 'length' : len(result)}, status = 200)
    return render(request, 'main/search_single.html')


@login_required
def GroupParticipants(request):
    if(request.is_ajax() and request.method == 'GET'):
        query = request.GET.getlist('participants[]')
        query.append(request.user.username)
        request.session['groupParticipants'] = query
        return JsonResponse({'valid' : True}, status = 200)
        
    return render(request, 'main/search_multiple.html')

@login_required
def GroupDetails(request):
    if(request.method == 'POST'):
        groupname = request.POST.get('groupname')
        return redirect('GroupView', groupname = groupname)
    return render(request, 'groups/groupdetail.html')