import wave
import contextlib
import os
import math
import numpy as np

def interpret_wav(raw_bytes, n_frames, n_channels, sample_width, interleaved=True):
    if sample_width == 1:
        dtype = np.uint8
    elif sample_width == 2:
        dtype = np.int16
    else:
        raise ValueError("Formats audio supportés : 8 ou 16 bits uniquement.")
    channels = np.frombuffer(raw_bytes, dtype=dtype)
    if interleaved:
        channels.shape = (n_frames, n_channels)
        channels = channels.T
    else:
        channels.shape = (n_channels, n_frames)
    return channels

def run_mean(x, windowSize):
    cumsum = np.cumsum(np.insert(x, 0, 0))
    return (cumsum[windowSize:] - cumsum[:-windowSize]) / windowSize


def process_audio(input_file, output_file, cutoff_frequency=1000.0):
    with contextlib.closing(wave.open(input_file, 'rb')) as spf:
        sampleRate = spf.getframerate()
        ampWidth = spf.getsampwidth()
        nChannels = spf.getnchannels()
        nFrames = spf.getnframes()

        signal = spf.readframes(nFrames * nChannels)
        spf.close()
        channels = interpret_wav(signal, nFrames, nChannels, ampWidth, True)

        fqRatio = cutoff_frequency / sampleRate
        N = int(math.sqrt(0.196196 + fqRatio**2) / fqRatio)

        filt = run_mean(channels[0], N).astype(channels.dtype)

        wav_file = wave.open(output_file, "w")
        wav_file.setparams((1, ampWidth, sampleRate, nFrames, spf.getcomptype(), spf.getcompname()))
        wav_file.writeframes(filt.tobytes('C'))
        wav_file.close()


def get_compression_info(original_file, filtered_file):
    original_size = os.path.getsize(original_file)
    filtered_size = os.path.getsize(filtered_file)
    compression_ratio = ((original_size - filtered_size) / original_size) * 100

    return {
        "original_size": original_size,
        "filtered_size": filtered_size,
        "compression_ratio": compression_ratio
    }
