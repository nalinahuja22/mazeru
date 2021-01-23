# Developed by matthew-notaro, nalinahuja22, and ClarkChan1

import os
import sys
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

class Audio:
    def __init__(self, afile):
        # Audio File Path
        self.afile = afile

        # Audio Analysis
        self.track = []

    def analyze(self):
        self.get_tempo()
        self.plot_audio()

    def get_tempo(self):
        # Audio File Duration
        duration = librosa.get_duration(filename = self.afile)

        # Iterate Over Audio
        for i in range(int(duration)):
            data, sr = librosa.load(self.afile, offset = i, duration = 1)
            onset = librosa.onset.onset_strength(data, sr = sr)
            tempo = librosa.beat.tempo(onset_envelope = onset, sr = sr)
            self.track.append(tempo[0])
        print(np.asarray(self.track))


    def plot_audio(self, start_seconds, end_seconds):
        # plot data
        data, sr = librosa.load(self.afile, offset=start_seconds,duration=end_seconds-start_seconds)
        time = (np.arange(0,len(data)) / sr) + start_seconds
        fig, ax = plt.subplots()
        ax.plot(time, data)
        ax.set(xlabel="time", ylabel="sound amplitude")
        plt.show()

obj = Audio("../media/audio/sensation.wav")
# obj.get_tempo()
obj.plot_audio(5,30)
