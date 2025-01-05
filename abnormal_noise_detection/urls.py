from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('noise-detection/', views.upload_and_detect, name='noise-detection')
]
