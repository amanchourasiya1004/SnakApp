from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import JsonResponse
from .models import PersonalChats, Friends, ImageUpload
from itertools import chain
import json
from usergroups.models import GroupChats, Groups, GroupUsers
from django.core.files.storage import FileSystemStorage

@login_required
def HomeView(request):
    finalchat = []
    # Group message section
    groupenrolled = request.user.groupenrolled.all()
    for i in groupenrolled:
        if(len(i.group.chats.all()) > 0):
            k1 = i.group.chats.latest('time')
        else:
            k1 = ''
        if(len(i.group.sentimages.all()) > 0):
            k2 = i.group.sentimages.latest('time')
        else:
            k2 = ''
        if(k1 == '' and k2 != ''):
            finalchat.append([i.group.groupname, '', k2.time, 1])
        elif(k1 != '' and k2 == ''):
            finalchat.append([i.group.groupname, k1.chats, k1.time, 0])
        elif(k1 != '' and k2 != ''):
            if(k1.time < k2.time):
                finalchat.append([i.group.groupname, '', k2.time, 1])
            else:
                finalchat.append([i.group.groupname, k1.chats, k1.time, 0])
    # Group message section end

    # Friends section start
    friends = list(chain(request.user.firstfriend.all(), request.user.secondfriend.all()))
    for i in friends:
        if(i.owner.username != request.user.username):
            name = i.owner.username
        else:
            name = i.friend.username
        if(len(i.friends.all()) > 0):
            k1 = i.friends.latest('time')
        else:
            k1 = ''
        if(len(i.sentimages.all()) > 0):
            k2 = i.sentimages.latest('time')
        else:
            k2 = ''
        if(k1 == '' and k2 != ''):
            finalchat.append([name, '', k2.time, 3])
        elif(k1 != '' and k2 == ''):
            finalchat.append([name, k1.chat, k1.time, 2])
        elif(k1 != '' and k2 != ''):
            if(k1.time < k2.time):
                finalchat.append([name, '', k2.time, 3])
            else:
                finalchat.append([name, k1.chat, k1.time, 2])
    # Friends section end

    sorted_chat = sorted(finalchat, key=lambda obj: obj[2], reverse=True)
    chat = []
    for i in sorted_chat:
        chat.append([i[0], i[1], i[3]])
    length = len(chat)
    chats = json.dumps(chat)
    return render(request, 'main/home.html', {'chats' : chats, 'length' : length})

@login_required
def SearchView(request):
    if(request.is_ajax() and request.method == 'GET'):
        query = request.GET.get('search', None)
        result = User.objects.filter(username__icontains = query)
        serialize_result = serializers.serialize('json', result)
        return JsonResponse({'result' : serialize_result, 'length' : len(result)}, status = 200)
    return render(request, 'main/search_single.html', {'me' : request.user.username})

@login_required
def personalChatView(request, name):
    arr = [request.user.username, name]
    arr.sort()
    if(len(Friends.objects.filter(owner__username = arr[0], friend__username = arr[1])) == 0):
        f = Friends.objects.create(owner = User.objects.get(username = arr[0]), friend = User.objects.get(username = arr[1]))
        total_msgs = []
    else:
        f = Friends.objects.get(owner__username = arr[0], friend__username = arr[1])
        messages = f.friends.all()
        images = f.sentimages.all()
        total_msgs = list(chain(messages, images))
        total_msgs = sorted(total_msgs, key=lambda obj: obj.time)
    if request.method == 'POST':
        try:
            print(request.FILES)
            myfile = request.FILES['data']
            fr = FileSystemStorage()
            filename = fr.save(myfile.name, myfile)
            print(filename, 'filename')
            url = fr.url(filename)
            print(url, 'url')
            ImageUpload.objects.create(path_image = url, filename = filename, chatconnect = f, sender = request.user.username)
            print('Image uploaded')
            return JsonResponse({'error': False, 'path': url})
        except:
            return JsonResponse({'error': True})
    return render(request, 'main/personalchat.html', {'otheruser' : name, 'me' : request.user.username, 'msgs' : total_msgs, 'length' : len(total_msgs)})

@login_required
def GroupParticipants(request):
    if(request.is_ajax() and request.method == 'GET'):
        query = request.GET.getlist('participants[]')
        query.append(request.user.username)
        request.session['groupParticipants'] = query
        return JsonResponse({'valid' : True}, status = 200)
        
    return render(request, 'main/search_multiple.html', {'me' : request.user.username})

@login_required
def GroupDetails(request):
    if(request.method == 'POST'):
        groupname = request.POST.get('groupname')
        return redirect('GroupCreate', groupname = groupname)
    return render(request, 'groups/groupdetail.html')

