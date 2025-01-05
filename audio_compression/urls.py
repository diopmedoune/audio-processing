from django.urls import path
from django.views.generic import TemplateView
from . import views


urlpatterns = [
    path('compression/', views.upload_and_compress, name='compression'),
]
