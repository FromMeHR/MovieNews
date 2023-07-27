from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('room/<str:pk>/', views.room, name="room"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),
    path('update-user/', views.updateUser, name="update-user"),
    path('password/', views.updatePassword, name="password"),
    path('topics/', views.topicsPage, name="topics"),
    path('allusers/', views.allUsers, name='all-users'),
    path('allmoderators/', views.allModerators, name='all-moderators'),
    path('update-moderator/', views.updateModerator, name='update-moderator'),
    path('activity/', views.activityPage, name="activity"),
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),
    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),
]