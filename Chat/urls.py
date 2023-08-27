from django.urls import path,include
from .views import *
urlpatterns = [
    path('',index,name='index'),
    path('<str:room_name>/',room,name='room'),
]
