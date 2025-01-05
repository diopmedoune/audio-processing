import numpy as np
import librosa
import soundfile as sf
from scipy.signal import wiener

# Méthode 1 : Filtrage fréquentiel (FFT)
def fft_filter(input_file, output_file, cutoff=1000):
    """
    Réduction de bruit avec filtrage fréquentiel (FFT)
    :param input_file: Chemin du fichier d'entrée
    :param output_file: Chemin du fichier de sortie
    :param cutoff: Fréquence de coupure pour le filtre passe-bas (en Hz)
    """
    y, sr = librosa.load(input_file, sr=None)
    fft_audio = np.fft.fft(y)
    freqs = np.fft.fftfreq(len(y), 1 / sr)

    # filtre passe-bas
    fft_audio[np.abs(freqs) > cutoff] = 0
    filtered_audio = np.fft.ifft(fft_audio).real
    sf.write(output_file, filtered_audio, sr)

# Méthode 2 : Filtre adaptatif (Wiener)
def wiener_filter(input_file, output_file, window_size=11):
    """
    Réduction de bruit avec filtre adaptatif (Wiener)
    :param input_file: Chemin du fichier d'entrée
    :param output_file: Chemin du fichier de sortie
    :param window_size: Taille de la fenêtre pour le filtre Wiener
    """
    y, sr = librosa.load(input_file, sr=None)
    # filtre Wiener
    filtered_audio = wiener(y, mysize=window_size)
    sf.write(output_file, filtered_audio, sr)
