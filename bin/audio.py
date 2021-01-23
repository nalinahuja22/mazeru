# Developed by matthew-notaro, nalinahuja22, and ClarkChan1

import os
import sys
import librosa
import matplotlib.pyplot as plt

def avg(l):
    return (sum(l) / len(l))

class Audio:
    def __init__(self, audio_file):
        # Audio File Path
        self.audio_file = audio_file

        # Audio Analysis
        self.track = []

    def analyze(self):
        duration = int(librosa.get_duration(filename = self.audio_file))

        l = []

        for i in range(duration):
            data, sr = librosa.load(self.audio_file, offset = i, duration = 1, mono = False)
            rms = (librosa.feature.rms(data))[0]

            l.append(avg(rms))

        plt.plot(l)
        plt.show()


obj = Audio("../media/audio/reminisce.wav")
obj.analyze()
