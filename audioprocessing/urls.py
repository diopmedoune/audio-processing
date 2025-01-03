from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='home'),

    # paths from apps
    path('', include("audio_compression.urls")),
    path('', include("abnormal_noise_detection.urls")),
    path('', include("audio_noise_reduction.urls")),
]
