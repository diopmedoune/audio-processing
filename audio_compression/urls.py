from django.urls import path
from django.views.generic import TemplateView
from . import views


urlpatterns = [
    path('compression/', TemplateView.as_view(template_name='audio_compression/compression.html'), name='compression'),
    path('upload/', views.upload_and_compress, name='upload_file'),
]
