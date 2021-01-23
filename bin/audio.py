# Developed by matthew-notaro, nalinahuja22, and ClarkChan1

import os
import sys
import wave as wv
import audioop as ap

class Audio:
    def __init__(self, audio_file):
        # Audio File Path
        self.audio_file = audio_file

        # Audio Analysis
        self.track = []

    def analyze(self):
        wf = wv.open(self.audio_file, "rb")
        for i in range(w.getnframes()):
            frame = w.readframes(i)
            print(ap.rms(frame))

obj = Audio("../media/audio/sensation.wav")
obj.analyze()
