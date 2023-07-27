from django.shortcuts import render, redirect
# from django.http import HttpResponse
from django.db.models import Q
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Room, Topic, Message, User
from .forms import RoomForm, UserForm, MyUserCreationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

def loginPage(request):
    page ='login'
    topics = Topic.objects.all()
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, "User doesn't exist")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username or password doesn't exist")
            
    context = {'page': page, 'topics': topics}    
    return render(request, 'base/login_registration.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = MyUserCreationForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "An error occured during registration")
    context = {'form': form, 'topics': topics}
    return render(request, 'base/login_registration.html', context)
    

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q)) # for choosing a topic
    check_is_superuser = request.user.is_superuser
    topics = Topic.objects.all()[0:4]
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))[0:3]
    
    selected_topic = None
    if q:
        selected_topic = q
    context = {'rooms':rooms, 'topics': topics, 'room_count': room_count, 'check_is_superuser': check_is_superuser, 'room_messages': room_messages, 'selected_topic': selected_topic, }
    return render(request, 'base/home.html', context)

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)
    topics = Topic.objects.all()
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            avatar_cleared = request.POST.get('avatar-clear', False)
            if avatar_cleared:
                user.avatar = 'avatar.svg'
            else:
                if 'avatar' in request.FILES:
                    user.avatar = request.FILES['avatar']
            form.save()
            return redirect('user-profile', pk=user.id)
    context = {'form': form, 'topics': topics}
    return render(request, 'base/update-user.html', context)

@login_required(login_url='login')
def updatePassword(request):
    user = request.user
    form = PasswordChangeForm(user=request.user)
    topics = Topic.objects.all()[0:4]
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.error(request, "Password updated successfully")
            return redirect('user-profile', pk=user.id)
        else:
            messages.error(request, "An error occured during updating password")
    context = {'form': form, 'topics': topics}
    return render(request, 'base/password.html', context)

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()[0:3]
    topics = Topic.objects.all()
    check_is_superuser = user.is_superuser
    context = {'user': user, 'check_is_superuser': check_is_superuser, 'rooms': rooms, 'room_messages': room_messages, 'topics': topics}
    return render(request, 'base/profile.html', context)

def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    context = {'topics': topics}
    return render(request, 'base/topics.html', context)

@login_required(login_url='login')
def allUsers(request):
    topics = Topic.objects.all()
    if not request.user.is_superuser:
        messages.error(request, "You're not superuser")
        return redirect('home')
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    users = User.objects.filter(username__icontains=q)
    context = {'users': users, 'topics': topics}
    return render(request, 'base/users.html', context)

@login_required(login_url='login')
def allModerators(request):
    topics = Topic.objects.all()
    if not request.user.is_superuser:
        messages.error(request, "You're not superuser")
        return redirect('home')
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    users = User.objects.filter(username__icontains=q)
    context = {'users': users, 'topics': topics}
    return render(request, 'base/moderators.html', context)

@login_required(login_url='login')
def updateModerator(request):
    if not request.user.is_superuser:
        messages.error(request, "You're not a superuser")
        return redirect('home')
    if request.method == 'POST':
        for user in User.objects.all():
            checkbox_name = f"moderator_{user.id}"
            is_moderator = checkbox_name in request.POST
            user.moderator = is_moderator
            user.save()
        messages.success(request, "Moderator status updated successfully")
    referer = request.META.get('HTTP_REFERER')
    if referer:
        if 'allmoderators' in referer:
            return redirect('all-moderators')
        elif 'allusers' in referer:
            return redirect('all-users')
    return redirect('home')


def activityPage(request):
    room_messages = Message.objects.all()
    context = {'room_messages': room_messages}
    return render(request, 'base/activity.html', context)

def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    room_photo = room.photo.url if room.photo else None
    if request.user.is_authenticated:
        room.viewers.add(request.user) 
    viewers = room.viewers.all()#[0:10]
    check_is_superuser = request.user.is_superuser
    topics = Topic.objects.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        return redirect('room', pk=room.id)
    context = {'room': room, 'check_is_superuser': check_is_superuser, 'room_messages': room_messages, 'viewers': viewers, 'topics': topics, 'room_photo': room_photo}
    return render(request, 'base/room.html', context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm
    topics = Topic.objects.all()
    if not (request.user.moderator or request.user.is_superuser): # for insurance if user try create through the link
        messages.error(request, "You're not superuser or moderator in order to create news")
        return redirect('home')
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES) 
        topic_name = request.POST.get('topic')
        topic, create = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
            photo = request.FILES.get('photo'),
        )
        return redirect('home')
        
    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if not (request.user.moderator or request.user.is_superuser): # for insurance if user try update through the link
        messages.error(request, "You're not superuser or moderator in order to update news")
        return redirect('home')
    if not (request.user.is_superuser or room.host.id == request.user.id ): # for insurance if moderator try update through the link
        messages.error(request, "Moderator can't update superuser's (or other moderators's) news")
        return redirect('home')
    if request.method == 'POST':
        form = RoomForm(request.POST, request.FILES, instance=room) 
        topic_name = request.POST.get('topic')
        topic, create = Topic.objects.get_or_create(name=topic_name)
        room.topic = topic
        room.name = request.POST.get('name')
        room.description = request.POST.get('description')
        room.photo = request.FILES.get('photo')
        room.save()
        return redirect('home')
    
    context = {'form': form, 'topics': topics,'room': room}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if not (request.user.moderator or request.user.is_superuser): # for insurance if user try delete through the link
        messages.error(request, "You're not superuser or moderator in order to delete news")
        return redirect('home')
    if not (request.user.is_superuser or room.host.id == request.user.id ): # for insurance if moderator try delete through the link
        messages.error(request, "Moderator can't delete superuser's (or other moderators's) news")
        return redirect('home')
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})

@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)
    if request.user != message.user:
        messages.error(request, "That's not your comment")
    if request.method == 'POST':
        message.delete()
        referring_page = request.POST.get('referring_page', '/')
        return redirect(referring_page)
    return render(request, 'base/delete.html', {'obj': message})

