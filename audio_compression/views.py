from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os

from audio_compression.compression import process_audio, get_compression_info


def upload_and_compress(request):
    if request.method == 'POST' and request.FILES['audio_file']:
        audio_file = request.FILES['audio_file']
        fs = FileSystemStorage()
        
        original_file_path = fs.save(audio_file.name, audio_file)
        original_file_full_path = fs.path(original_file_path)
        
        original_file_url = fs.url(original_file_path)
        
        compressed_file_name = f"compressed_{audio_file.name}"
        compressed_file_path = os.path.join(settings.MEDIA_ROOT, compressed_file_name)
        
        process_audio(original_file_full_path, compressed_file_path)
        
        compression_info = get_compression_info(original_file_full_path, compressed_file_path)
        
        context = {
            'original_file_url': original_file_url,
            'compressed_file_url': fs.url(compressed_file_name),
            'compression_info': compression_info,
        }

        return render(request, 'audio_compression/compression.html', context=context)

    return render(request, 'audio_compression/compression.html')
