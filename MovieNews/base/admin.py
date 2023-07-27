from django.contrib import admin
from .models import Room, Topic, Message, User
# Register your models here.

# admin.site.register(Room) 

@admin.register(User)
class UserModel(admin.ModelAdmin):
    list_filter = ('name','email','avatar','moderator')
    list_display = ('name','email','avatar','moderator')
@admin.register(Room)
class RoomModel(admin.ModelAdmin):
    list_filter = ('name','description','created','host','topic','created','photo')
    list_display = ('name','description','created','host','topic','created','photo')
@admin.register(Topic)
class TopicModel(admin.ModelAdmin):
    list_filter = ('name',)
    list_display = ('name',)
@admin.register(Message)
class MessageModel(admin.ModelAdmin):
    list_filter = ('user','body','created','room')
    list_display = ('user','body','created','room')
