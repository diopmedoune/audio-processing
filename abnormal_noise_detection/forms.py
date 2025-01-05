from django import forms

class AudioUploadForm(forms.Form):
    audio_file = forms.FileField(label="Charger le fichier audio", required=False)
    threshold = forms.FloatField(label='Seuil', initial=1.9, min_value=0.1, max_value=5.0, required=False)