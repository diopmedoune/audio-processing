from django.urls import path
from . import views

urlpatterns = [
    path('audio_denoise/', views.audio_denoise, name='audio_denoise'),
]
