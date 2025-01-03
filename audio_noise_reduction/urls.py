from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('noise-reduction/', TemplateView.as_view(template_name='audio_noise_reduction/noise_reduction.html'), name='noise-reduction')
]
