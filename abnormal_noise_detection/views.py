from django.shortcuts import render
from django.http import HttpResponse
from .forms import AudioUploadForm
from .anormal import detect_anomalies, plot_results
from scipy.io.wavfile import read
import base64
import numpy as np
from io import BytesIO
from pydub import AudioSegment
from pydub import AudioSegment
import io
from django.core.files.uploadedfile import InMemoryUploadedFile

def convert_to_wav(audio_data):
    audio_file = io.BytesIO(audio_data)
    # Utiliser pydub pour charger et convertir en WAV
    audio_segment = AudioSegment.from_file(audio_file)
    audio_wav = io.BytesIO()
    audio_segment.export(audio_wav, format="wav")
    audio_wav.seek(0)  # Repositionner le pointeur de lecture au début du fichier WAV
    return audio_wav

def upload_and_detect(request):
    if request.method == 'POST':
        form = AudioUploadForm(request.POST, request.FILES)
        if 'audio_file' in request.FILES:
            if form.is_valid():
                audio_file = request.FILES['audio_file']

                threshold = form.cleaned_data['threshold']

                try:
                    sample_rate, audio = read(audio_file)
                    if len(audio.shape) > 1:
                        audio = np.mean(audio, axis=1)

                    anomalies, energy, frame_size, step_size = detect_anomalies(audio, sample_rate, threshold)

                    buffer = plot_results(audio, sample_rate, anomalies, energy, frame_size, step_size)
                    
                    image_png = buffer.getvalue()
                    graphic = base64.b64encode(image_png).decode('utf-8')
                    buffer.close()

                    return render(request, 'abnormal_noise_detection/resultats.html', {'chart': graphic, 'threshold': threshold})

                except Exception as e:
                    return render(request, 'abnormal_noise_detection/noise_detection.html', {
                        'form': form,
                        'error': f"Erreur lors du traitement du fichier audio : {e}"
                    })


                
        elif 'audio_data' in request.POST:
            # Récupérer l'audio envoyé en base64
            audio_data = request.POST.get('audio_data')
            threshold = float(request.POST.get('threshold', 1.9))
            
            # Décoder l'audio depuis base64
            audio_data = base64.b64decode(audio_data)
            audio_file = BytesIO(audio_data)
            

            try:
                # Vérifiez que le fichier est bien un WAV en lisant l'entête
                header = audio_file.read(4)
                audio_file.seek(0)  # Remettez le pointeur au debut

                if header not in [b'RIFF', b'RIFX']:
                    raise ValueError("Le fichier fourni n'est pas un fichier WAV valide.")

                # Lire le fichier WAV avec scipy
                sample_rate, audio = read(audio_file)

                # Si l'audio est stéréo, le convertir en mono
                if len(audio.shape) > 1:
                    audio = np.mean(audio, axis=1)

                # Appliquer le traitement sur l'audio (détection des anomalies, etc.)
                anomalies, energy, frame_size, step_size = detect_anomalies(audio, sample_rate, threshold=1.9)

                # Générer le graphique des anomalies
                buffer = plot_results(audio, sample_rate, anomalies, energy, frame_size, step_size)

                # Encoder l'image en base64 pour l'afficher dans le template
                image_png = buffer.getvalue()
                graphic = base64.b64encode(image_png).decode('utf-8')
                buffer.close()

                return render(request, 'abnormal_noise_detection/resultats.html', {
                    'chart': graphic,
                    'threshold': threshold
                })

            except Exception as e:
                return render(request, 'abnormal_noise_detection/noise_detection.html', {
                    'error': f"Erreur lors du traitement du fichier audio : {str(e)}"
                })

    else:
        form = AudioUploadForm()

    return render(request, 'abnormal_noise_detection/noise_detection.html', {'form': form})