from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView, name = 'HomeView'),
    path('search/username/', views.SearchView, name = 'SearchView'),
    path('group/participants/', views.GroupParticipants, name = 'GroupParticipants'),
    path('personalchat/<name>/', views.personalChatView, name = 'PersonalChat'),
    path('group/detail/', views.GroupDetails, name = 'GroupDetails'),
    path('image/send/', views.ImageProcess, name = 'ImageProcess'),

]