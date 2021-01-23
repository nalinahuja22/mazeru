# Developed by matthew-notaro, nalinahuja22, and ClarkChan1

import os
import sys
import librosa

class Audio:
    def __init__(self, audio_file):
        # Audio File Path
        self.audio_file = audio_file

        # Audio Analysis
        self.track = []

    def analyze(self):
        data, sr = librosa.load(self.audio_file, mono = False)

        print(data)


obj = Audio("../media/audio/wav/reminisce.wav")
obj.analyze()
