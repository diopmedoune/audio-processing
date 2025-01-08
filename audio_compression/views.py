from django.shortcuts import render
import os
from .compression import process_audio, get_compression_info
from audio_compression.templatetags.custom_filters import bytes_to_mb
from pydub import AudioSegment

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
        output_format = request.POST.get('output_format', 'WAV').lower()

        temp_dir = 'media/temp/'
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        input_path = os.path.join(temp_dir, audio_file.name)
        base_name = os.path.splitext(audio_file.name)[0]
        output_path = os.path.join(temp_dir, f"compressed_{base_name}.{output_format}")

        with open(input_path, 'wb+') as temp_file:
            for chunk in audio_file.chunks():
                temp_file.write(chunk)

        # Traitement de l'audio
        process_audio(input_path, output_path, cutoff_frequency)

        # Conversion au format MP3 si nécessaire
        if output_format == 'mp3':
            mp3_path = os.path.join(temp_dir, f"compressed_{base_name}.mp3")
            audio = AudioSegment.from_wav(output_path)
            audio.export(mp3_path, format="mp3")
            output_path = mp3_path

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
