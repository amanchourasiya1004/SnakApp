from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .models import Users, ProfilePic
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
import random
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
from django.core import serializers

# Create your views here.
def RegisterView(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password')
        if len(User.objects.filter(username=uname)) == 0 and len(User.objects.filter(email=email)) == 0:
            code = str(random.randint(1000, 10000))
            to_email = email
            send_mail(
                'sender_mail', 
                code,
                'amanchourasiya1004@gmail.com',
                [to_email], 
                fail_silently=False,
            )
            request.session['code'] = code
            request.session['name'] = uname
            request.session['email'] = email
            request.session['pass'] = password1
            return redirect('ConfirmEmailView')
        else:
            return HttpResponse('Username already taken. Try another.')
    return render(request, 'users/register.html')

def ConfirmEmailView(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        if code == request.session['code']:      
            uname = request.session['name']
            password1 = request.session['pass']
            email = request.session['email']
            hashed_pwd = make_password(password1)
            Users.objects.create(username = uname, email = email , password = hashed_pwd)
            user = User.objects.create_user(username=uname,email=email,password=password1)
            user.save()
            user = authenticate(username = uname , password = password1)
            login(request, user)
            return redirect("SaveProfilePic")
        else:
            return render(request, 'users/confirm_email.html', {'msg' : 'Wrong PIN. Try again..'})
    return render(request, 'users/confirm_email.html', {'msg' : ''})

def LoginView(request):
    if(request.user.is_authenticated):
        return render(request, 'main/home.html')
    if request.method == "POST":
        uname = request.POST.get('username')
        password = request.POST.get('password')
        if(uname != "" and password != ""):
            user = authenticate(username = uname, password = password)
            if(user != None):
                login(request, user)
                return redirect('HomeView')
        else:
            return render(request, 'users/login.html', {'msg' : 'Something wrong'})
    return render(request, 'users/login.html', {'msg' : ''})

@login_required(login_url = '')
def LogoutView(request):
    logout(request)
    return redirect('RegisterView')

def SaveProfilePic(request):
    if (request.method == 'POST' and request.is_ajax()):
        
        print(request.FILES)
        myfile = request.FILES['data']
        a = ProfilePic(img = myfile, user = request.user.username)
        a.save()
        return JsonResponse({'error': False})
            # return JsonResponse({'error': True})
    elif(request.method == "POST"):
        
        first = request.POST.get('first')
        last = request.POST.get('last')
        user = User.objects.get(username = request.user.username)
        user.first_name = first
        user.last_name = last
        user.save()
        return redirect("HomeView")
    return render(request, 'users/extrapersonal.html')


