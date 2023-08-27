from django.shortcuts import render

# Create your views here.

def index (request):
    return render(request,'Chat/index.html')

def room(request,room_name):
    context={
        'room_name': room_name
    }
    return render(request,'Chat/room.html',context)