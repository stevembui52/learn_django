from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Room, Topic
from .form import RoomForm
# Create your views here.


# rooms = [
#     {"id":1, "name": "Study javascript easy way"},
#     {"id":2, "name": "Learning software engineering"},
#     {"id":3, "name": "Developing desktop apps"}
# ]

def home(request):
    q = request.GET.get('q') if q == request.GET.get('q') !=None else ''
    rooms = Room.objects.filter(topic__name__icontains = q)
    topics = Topic.objects.all()

    context = {"rooms":rooms, "topics":topics}

    return render(request, 'base/index.html', context)


def room(request, pk):
    # return HttpResponse("rooms template here")
    # room =None
    # for aroom in rooms:
    #     if aroom.get("id") == int(pk):
    #         room = aroom
    #         context = {"room":room}
    room = Room.objects.get(id = pk)
    context = {"room":room}
    return render(request, 'base/room.html', context)


def create_room(request):
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {"form":form}
    return render(request, 'base/room_form.html', context)


def update_room(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.method == "POST":
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {"form": form}
    return render(request, 'base/room_form.html', context)

def delete_room(request, pk):
    room = Room.objects.get(id=pk)
    
    
    if request.method == "POST":
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {"obj":room})