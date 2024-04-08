from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('room/<int:pk>/', views.room, name="room"),
    path('create_room', views.create_room, name="create_room"),
    path('update_room/<int:pk>', views.update_room, name="update_room"),
    path('delete_room/<int:pk>', views.delete_room, name="delete_room")
]