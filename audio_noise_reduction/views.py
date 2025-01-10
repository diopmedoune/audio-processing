from django.http import JsonResponse
from django.shortcuts import render
import noisereduce as nr
import librosa
import soundfile as sf
import os
from django.conf import settings


def audio_denoise(request):
    if request.method == 'POST' and request.FILES.get('audio_file'):
        try:
            # Récupérer le fichier audio et le format
            audio_file = request.FILES['audio_file']
            audio_format = request.POST.get('audio_format', 'wav')

            # Sauvegarder le fichier audio dans le répertoire 'media'
            media_dir = os.path.join(settings.MEDIA_ROOT, 'audio_files')
            os.makedirs(media_dir, exist_ok=True)
            file_path = os.path.join(media_dir, f"temp_audio.{audio_format}")
            with open(file_path, 'wb') as f:
                for chunk in audio_file.chunks():
                    f.write(chunk)

            # Charger et débruiter l'audio
            y, sr = librosa.load(file_path, sr=None)
            if y is None or len(y) == 0:
                raise ValueError("Le fichier audio est vide ou corrompu.")

            y_denoised = nr.reduce_noise(y=y, sr=sr)
            if y_denoised is None or len(y_denoised) == 0:
                raise ValueError("La réduction du bruit a échoué ou a produit un résultat vide.")

            # Sauvegarder l'audio débruité dans 'media'
            denoised_path = os.path.join(media_dir, f"denoised_audio.{audio_format}")
            sf.write(denoised_path, y_denoised, sr)
            if not os.path.exists(denoised_path):
                raise ValueError(f"Le fichier débruité n'a pas pu être écrit à {denoised_path}.")

            # Retourner les résultats avec le chemin relatif
            return JsonResponse({
                'original_audio_url': os.path.join(settings.MEDIA_URL, 'audio_files', f"temp_audio.{audio_format}"),
                'denoised_audio_url': os.path.join(settings.MEDIA_URL, 'audio_files', f"denoised_audio.{audio_format}"),
            })

        except Exception as e:
            # En cas d'erreur, retourner un message d'erreur
            return JsonResponse({'error': str(e)}, status=500)

    return render(request, 'audio_noise_reduction/noise_reduction.html')


