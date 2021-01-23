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
        self.plot_audio(0,2)

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
        # time = (np.arange(0,len(data)) / sr)
        fig, ax = plt.subplots(nrows=2, sharex=True)
        # set up plot for raw audio
        ax[0].set(title='raw audio')
        ax[0].plot(time, data)
        ax[0].set(ylabel="sound amplitude")

        # print global max sound amplitude
        print(max(data))

        # set up plot for beat timestamp estimation
        onset_env = librosa.onset.onset_strength(y=data, sr=sr)
        pulse = librosa.beat.plp(onset_envelope=onset_env, sr=sr)
        beats_plp = np.flatnonzero(librosa.util.localmax(pulse))
        time = librosa.times_like(pulse, sr=sr) + start_seconds
        # time = librosa.times_like(pulse, sr=sr)
        ax[1].set(title='estimated beats')
        ax[1].set(xlabel="time", ylabel="sound amplitude")
        ax[1].plot(time, librosa.util.normalize(pulse), label='PLP')
        ax[1].vlines(time[beats_plp], 0, 1, alpha=0.5, color='r', linestyle='--', label='PLP Beats')
        ax[1].legend()

        # print beat timestamps
        print(time[beats_plp])

        # show the plots
        plt.show()

obj = Audio("../media/audio/sensation.wav")
# obj.analyze()
obj.plot_audio(0,2)
