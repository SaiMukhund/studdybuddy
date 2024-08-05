from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
# Create your views here.
from .models import Room ,Topic,Message
from .forms import RoomForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators  import login_required

def login_page(request):
    page="login"
    if request.user.is_authenticated:
        return redirect('home')

    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")

        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request,"User not found" )
        
        user=authenticate(request,username=username,password=password)
        if user is not None :
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"user or password doesnt match")
    context={"page":page}
    return render(request,'base/login_register.html',context)
def register_user(request):
    page="register"
    form=UserCreationForm()
    if request.method=="POST":
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request,user)
            return render(request,'home')
        else:
            messages.error(request,"an error occured during registration")
    context={"page":page,"form":form}
    return render(request,'base/login_register.html',context)

def logout_user(request):
    logout(request)
    return redirect('home')

def home(request):
    q=request.GET.get('q',"")
    rooms=Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    topics=Topic.objects.all()
    room_count=rooms.count()
    all_messages=Message.objects.filter(Q(room__name__icontains=q))
    context={"rooms":rooms,"topics":topics,"room_count":room_count,"all_messages":all_messages}
    return render(request,"base/home.html",context)

def room(request,pk):
    room=Room.objects.get(id=pk)
    room_messages=room.message_set.all().order_by("-created")
    participants=room.participants.all()
    if request.method=="POST":
        room_message=Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room',pk=room.id)
    context={"room":room,"messages":room_messages,"participants":participants}
    return render(request,"base/room.html",context)

@login_required(login_url='/login_page')
def createRoom(request):
    form=RoomForm()
    if request.method=="POST":
        form=RoomForm(request.POST)
        if form.is_valid():
            room=form.save(commit=False)
            room.host=request.user
            room.save()
            room.participants.add(request.user)
            return redirect('home')
    context={'form':form}
    return render(request,'base/form.html',context)

@login_required(login_url="/login_page")
def updateRoom(request,pk):
    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room)
    if request.user != room.host:
        return HttpResponse("You are not the user")

    if request.method=="POST":
        form=RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={"form":form}
    return render(request,'base/form.html',context)
@login_required(login_url="/login_page")
def deleteRoom(request,pk):
    room=Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse("You are not the user")
    if request.method=="POST":
        room.delete()
        return redirect("home")
    return render(request,'base/delete.html',{"obj":room.name})

@login_required(login_url="/login_page")
def deleteMessage(request,pk):
    mess=Message.objects.get(id=pk)
    if request.user != mess.user:
        return HttpResponse("You are not the user")
    if request.method=="POST":
        mess.delete()
        return redirect("home")
    return render(request,'base/delete.html',{"obj":mess})

def userProfile(request,pk):
    profile=User.objects.get(id=pk)
    rooms=profile.room_set.all()
    user_messages=profile.message_set.all()
    user_topics=Topic.objects.all()
    context={"profile":profile,"rooms":rooms,"topics":user_topics,"all_messages":user_messages}
    return render(request,'base/profile.html', context )