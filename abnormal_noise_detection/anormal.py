import sounddevice as sd
import numpy as np
import soundfile as sf
import io
from scipy.io.wavfile import read
from scipy.signal import spectrogram
import matplotlib.pyplot as plt

def enregistre(nom, duration=16):
    # Paramètres d'enregistrement
    # Durée en secondes
    fs = 44100  # Fréquence d'échantillonnage
    print("Enregistrement...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float64')
    sd.wait()  # Attendre la fin de l'enregistrement
    print("Enregistrement terminé.")

    file_path = f"C:/Users/DELL/Desktop/Projet_Signal/Audios/{nom}.wav"  # Mets ton propre chemin ici
    sf.write(file_path, audio, fs)
    print(f"Enregistrement sauvegardé dans '{file_path}'")

    print("Lecture de l'enregistrement...")
    sd.play(audio, samplerate=fs)  # Lecture de l'audio
    sd.wait()  # Attendre la fin de la lecture
    print("Lecture terminée.")





def detect_anomalies(audio, sample_rate, threshold=1.9):
    # Calculer l'énergie locale en utilisant des fenêtres
    frame_size = int(0.1 * sample_rate)  # Fenêtre de 100ms
    step_size = int(frame_size / 2)
    energy = []
    
    for i in range(0, len(audio) - frame_size, step_size):
        frame = audio[i:i+frame_size]
        energy.append(np.sum(frame**2))  # Énergie du signal
    
    energy = np.array(energy)
    mean_energy = np.mean(energy)
    std_energy = np.std(energy)
    
    # Détecter les frames où l'énergie dépasse le seuil
    anomalies = np.where(energy > mean_energy + threshold * std_energy)[0]
    
    # Convertir les indices d'anomalies en temps
    times = anomalies * (step_size / sample_rate)
    return times, energy, frame_size, step_size


def plot_results(audio, sample_rate, anomalies, energy, frame_size, step_size):
    time_audio = np.linspace(0, len(audio) / sample_rate, num=len(audio))
    
    plt.figure(figsize=(14, 8))
    
    # Tracé du signal audio
    plt.subplot(2, 1, 1)
    plt.plot(time_audio, audio, label="Signal audio", color='mediumblue', linewidth=1.5)
    plt.title("Signal audio avec anomalies détectées", fontsize=16, fontweight='bold', family='serif', color='darkblue')
    plt.xlabel("Temps (s)", fontsize=12, fontstyle='italic', color='black')
    plt.ylabel("Amplitude", fontsize=12, fontweight='normal', color='darkgreen')
    plt.grid(True, linestyle='--', alpha=0.7)
    for anomaly_time in anomalies:
        plt.axvline(x=anomaly_time, color='r', linestyle='--')
        
    plt.legend(loc="upper right", fontsize=12)
    
    # Tracé de l'énergie
    plt.subplot(2, 1, 2)
    energy_time = np.arange(len(energy)) * (step_size / sample_rate)
    plt.plot(energy_time, energy, label="Énergie", color='darkorange', linewidth=2)
    plt.title("Énergie du signal", fontsize=16, fontweight='bold', family='serif', color='darkred')
    plt.xlabel("Temps (s)", fontsize=12)
    plt.ylabel("Énergie", fontsize=12)
    plt.axhline(np.mean(energy), color='green', linestyle='--', label="Énergie moyenne")
    plt.legend(loc="upper right", fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    
    # Enregistrer dans un buffer et le retourner
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=300)
    buffer.seek(0)
    plt.close()
    
    return buffer
