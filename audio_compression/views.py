from django.shortcuts import render
import os
from .compression import process_audio, get_compression_info
from audio_compression.templatetags.custom_filters import bytes_to_mb

def upload_and_compress(request):
    compression_info = None
    default_frequency = 1000
    compressed_file_url = None
    original_file_url = None

    context = {
        'compression_info': compression_info,
        'default_frequency': default_frequency,
        'original_file_url': original_file_url,
        'compressed_file_url': compressed_file_url,
    }
    
    if request.method == 'POST' and request.FILES.get('audio_file'):
        audio_file = request.FILES['audio_file']
        cutoff_frequency = float(request.POST.get('cutoff_frequency', default_frequency))

        temp_dir = 'media/temp/'
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        input_path = os.path.join(temp_dir, audio_file.name)
        output_path = os.path.join(temp_dir, f"compressed_{audio_file.name}")

        with open(input_path, 'wb+') as temp_file:
            for chunk in audio_file.chunks():
                temp_file.write(chunk)

        process_audio(input_path, output_path, cutoff_frequency)
        compression_info = get_compression_info(input_path, output_path)

        original_file_url = f"/{input_path}"
        compressed_file_url = f"/{output_path}"

        context = {
            'compression_info': compression_info,
            'default_frequency': default_frequency,
            'original_file_url': original_file_url,
            'compressed_file_url': compressed_file_url,
        }
        return render(request, 'audio_compression/success_compression.html', context=context)
    
    return render(request, 'audio_compression/compression.html', context=context)
