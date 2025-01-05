import librosa
import soundfile as sf
import numpy as np

def reduce_noise_fft(input_file, output_file):
    y, sr = librosa.load(input_file, sr=None)
    y_fft = np.fft.rfft(y)
    y_fft[np.abs(y_fft) < 0.1 * max(np.abs(y_fft))] = 0
    y_filtered = np.fft.irfft(y_fft)
    sf.write(output_file, y_filtered, sr)

def reduce_noise_adaptive(input_file, output_file):
    y, sr = librosa.load(input_file, sr=None)
    noise_profile = np.mean(y[:int(0.5 * sr)])  # Supposons que le bruit est dans les 0.5 premières secondes
    y_denoised = y - noise_profile
    sf.write(output_file, y_denoised, sr)
