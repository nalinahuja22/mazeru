# Developed by matthew-notaro, nalinahuja22, and ClarkChan1

import scipy
import librosa

from collections import deque

# End Imports----------------------------------------------------------------------------------------------------------------------------------------------------------

# Distance Between Audio Peaks (ms)
PEAK_DIST = 50

# End Constants--------------------------------------------------------------------------------------------------------------------------------------------------------

class Audio:
    def __init__(self, file):
        # Audio File Path
        self.file = file

        # Audio Metadata
        self.sample_rate = None
        self.frame_count = None
        self.duration = None
        self.peaks = None

    def analyze(self):
        print("starting audio processing...")

        # Load Audio File
        wf, sr = librosa.load(self.file)

        # Populate Audio Metadata
        self.frame_count = len(wf)
        self.sample_rate = sr

        self.duration = librosa.get_duration(y = wf)

        # Process Negative Audio Data
        for i in range(len(wf)):
            # Zero Negative Peaks
            if (wf[i] < 0):
                wf[i] = 0

        # Compute Minimum Audio Peak Distance
        min_dist = (sr // (1000 // PEAK_DIST))

        # Process Waveform Peaks
        self.peaks = (list(scipy.signal.find_peaks(wf, distance = min_dist)[0]))

        print("ending audio processing...")

# End Class-------------------------------------------------------------------------------------------------------------------------------------------------------------
