from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('register/', views.register_user, name="register"),
    path('', views.home, name="home"),
    path('room/<int:pk>/', views.room, name="room"),
    path('create_room', views.create_room, name="create_room"),
    path('update_room/<int:pk>', views.update_room, name="update_room"),
    path('delete_room/<int:pk>', views.delete_room, name="delete_room"),
    path('delete_message/<int:pk>', views.delete_message, name="delete_message"),
]