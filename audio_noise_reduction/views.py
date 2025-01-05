import os
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from django.core.files.storage import default_storage
from .noise_reduction import fft_filter, wiener_filter

def noise_reduction(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES.get('audio_file')
        method = request.POST.get('method')

        if uploaded_file:
            original_file_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)
            with open(original_file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            processed_file_name = f"processed_{uploaded_file.name}"
            processed_file_path = os.path.join(settings.MEDIA_ROOT, processed_file_name)

            if method == "fft":
                fft_filter(original_file_path, processed_file_path)
            elif method == "adaptive":
                wiener_filter(original_file_path, processed_file_path)

            context['original_file_url'] = f"{settings.MEDIA_URL}{uploaded_file.name}"
            context['processed_file_url'] = f"{settings.MEDIA_URL}{processed_file_name}"

    return render(request, 'audio_noise_reduction/noise_reduction.html', context)
