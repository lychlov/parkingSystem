from django.urls import path
from . import views

urlpatterns = [
    path('GetFaceData', views.HeartBeatHandler.as_view()),
]
