from django.urls import path
from camera import views

urlpatterns = [
    path("stream", views.stream, name="stream"),
    path("live", views.live, name="live"),
    path("playback", views.playback, name="playback"),
    path("setting", views.setting, name="setting"),
]
