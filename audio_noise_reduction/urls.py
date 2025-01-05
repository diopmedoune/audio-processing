from django.urls import path
from . import views

urlpatterns = [
    path('noise-reduction/', views.noise_reduction, name='noise_reduction'),
]
