# Developed by matthew-notaro, nalinahuja22, and ClarkChan1

import os
import sys

class Audio:
    def __init__(self, afile):
        # Audio File Path
        self.afile = afile

        # Audio Analysis
        self.track = []

    def analyze(self):
        # Audio File Duration
        duration = librosa.get_duration(filename = self.afile)

        # Iterate Over Audio
        for i in range(int(duration)):
            data, sr = librosa.load(self.afile, offset = i, duration = 1)

            onset = librosa.onset.onset_strength(data, sr = sr)

            tempo = librosa.beat.tempo(onset_envelope = onset, sr = sr)

            print(tempo)

obj = Audio("../media/audio/solstice.mp3")

obj.analyze()
