from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.db.models import Q
from .models import Room, Topic, Message
from .form import RoomForm
# Create your views here.


# rooms = [
#     {"id":1, "name": "Study javascript easy way"},
#     {"id":2, "name": "Learning software engineering"},
#     {"id":3, "name": "Developing desktop apps"}
# ]

def login_user(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username')
        password= request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist")

        auth_user = authenticate(request, username=username, password=password)
        if auth_user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Incorrect creds")
    context = {'page':page}
    return render(request, 'base/register_login.html', context)


def logout_user(request):
    logout(request)
    return redirect('login')

def register_user(request):
    form = UserCreationForm()
    
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, "registered successifully")
            return redirect('home')
        else:
            messages.error(request, "An error ocurred during registration")
            
    context={"form":form}
    return render(request, 'base/register_login.html', context)


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains = q) |
        Q(name__icontains = q) |
        Q(description__icontains = q))
    topics = Topic.objects.all()

    room_count = rooms.count()
    room_message = Message.objects.all()
    context = {"rooms":rooms, "topics":topics, "room_count":room_count, "room_messages":room_message}

    return render(request, 'base/index.html', context)


def room(request, pk):
    # return HttpResponse("rooms template here")
    # room =None
    # for aroom in rooms:
    #     if aroom.get("id") == int(pk):
    #         room = aroom
    #         context = {"room":room}
    room = Room.objects.get(id = pk)
    room_messages = room.message_set.all()
    participant = room.participants.all()
    if request.method == "POST":
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get("msg_body")
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)
    context = {"room":room, "room_messages":room_messages, "participants":participant}
    return render(request, 'base/room.html', context)

@login_required(login_url='login')
def create_room(request):
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {"form":form}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)


    if request.user != room.host:
        return HttpResponse("NOT ALLOWED HERE!")
    
    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {"form": form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def delete_room(request, pk):
    room = Room.objects.get(id=pk)
    
    if request.user != room.host:
        return HttpResponse("NOT ALLOWED HERE!")
    
    if request.method == "POST":
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {"obj":room})

@login_required(login_url='login')
def delete_message(request, pk):
    message = Message.objects.get(id=pk)
    
    if request.user != message.user:
        return HttpResponse("NOT ALLOWED HERE!")
    
    if request.method == "POST":
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {"obj":message})