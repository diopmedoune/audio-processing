import os
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from django.core.files.storage import default_storage
from .noise_reduction import reduce_noise_fft, reduce_noise_adaptive

def noise_reduction(request):
    context = {}
    if request.method == 'POST':
        # Récupérer le fichier téléchargé
        uploaded_file = request.FILES.get('audio_file')
        method = request.POST.get('method')

        if uploaded_file:
            # Sauvegarder le fichier
            original_file_path = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)
            with open(original_file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            # Traiter le fichier selon la méthode choisie
            processed_file_name = f"processed_{uploaded_file.name}"
            processed_file_path = os.path.join(settings.MEDIA_ROOT, processed_file_name)

            if method == "fft":
                reduce_noise_fft(original_file_path, processed_file_path)
            elif method == "adaptive":
                reduce_noise_adaptive(original_file_path, processed_file_path)

            # Ajouter les fichiers au contexte
            context['original_file_url'] = f"{settings.MEDIA_URL}{uploaded_file.name}"
            context['processed_file_url'] = f"{settings.MEDIA_URL}{processed_file_name}"

    return render(request, 'audio_noise_reduction/noise_reduction.html', context)
