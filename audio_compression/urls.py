from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('compression/', TemplateView.as_view(template_name='audio_compression/compression.html'), name='compression')
]
