from django.shortcuts import render
from django.http import JsonResponse
import os
from .noise_reduction import fft_filter, wiener_filter

def audio_denoise(request):
    if request.method == 'POST' and request.FILES.get('audio_file'):
        audio_file = request.FILES['audio_file']
        method = request.POST.get('method', 'fft')
        cutoff_frequency = float(request.POST.get('cutoff_frequency', 1000))
        window_size = int(request.POST.get('window_size', 11))
        temp_dir = 'media/temp/'
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        input_path = os.path.join(temp_dir, audio_file.name)
        base_name, ext = os.path.splitext(audio_file.name)
        output_path = os.path.join(temp_dir, f"denoised_{base_name}.wav")
        with open(input_path, 'wb+') as temp_file:
            for chunk in audio_file.chunks():
                temp_file.write(chunk)
        if method == 'fft':
            fft_filter(input_path, output_path, cutoff=cutoff_frequency)
        elif method == 'wiener':
            wiener_filter(input_path, output_path, window_size=window_size)
        return JsonResponse({
            'original_audio_url': f"/{input_path}",
            'denoised_audio_url': f"/{output_path}"
        })
    return render(request, 'audio_noise_reduction/noise_reduction.html')
