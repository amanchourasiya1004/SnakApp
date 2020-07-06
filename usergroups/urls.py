from django.urls import path
from . import views

urlpatterns = [
    path('<groupname>/', views.GroupView, name = 'GroupView'),
]