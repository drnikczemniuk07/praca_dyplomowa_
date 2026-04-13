import numpy as np 
import librosa
import json 

NOTES = ["C", "C#", "D", "D#", "E", "F",
         "F#", "G", "G#", "A", "A#", "B"]

#y-fala dzwiekowa 
#sr- sample rate 
def extract_features(path: str) -> dict: 
    y, sr = librosa.load(path)
    duration = len(y)/sr
    rms = librosa.feature.rms(y=y)
    rolloff = librosa.feature.spectral_rolloff(y=y,sr=sr)
    onset = librosa.onset.onset_strength(y=y,sr=sr)
    tempo, beats  = librosa.beat.beat_track(onset_envelope=onset, sr=sr)
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    rolloff_mean = rolloff.mean()
    rms_mean = rms.mean()
    centroid = librosa.feature.spectral_centroid(y=y,sr=sr)
    centroid_mean = centroid.mean()
    chroma_mean = chroma.mean(axis=1)
    key_index  = chroma_mean.argmax()
    key = NOTES[key_index]
    return{ "duration_sec": duration,
            "rms_mean": float(rms_mean),
            "spectral_centroid_mean_hz": float(centroid_mean),
            "spectral_rolloff_mean_hz" : float(rolloff_mean),
            "tempo_bpm" : float(tempo[0]),
            "key" : key
            
    }
if __name__ == "__main__":
        result = extract_features("test.wav")
        print(json.dumps(result, indent=2))  

