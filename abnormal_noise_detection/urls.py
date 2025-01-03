from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('noise-detection/', TemplateView.as_view(template_name='abnormal_noise_detection/noise_detection.html'), name='noise-detection')
]
