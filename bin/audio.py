# Developed by matthew-notaro, nalinahuja22, and ClarkChan1

import scipy
import librosa

from collections import deque

# End Imports----------------------------------------------------------------------------------------------------------------------------------------------------------

# Distance Between Audio Peaks (ms)
PEAK_DIST = 250

# End Constants--------------------------------------------------------------------------------------------------------------------------------------------------------

class Audio:
    def __init__(self, file):
        # Audio File Path
        self.file = file

        # Audio Metadata
        self.sr = None
        self.fn = None

    def analyze(self):
        # Load Audio File
        wf, sr = librosa.load(self.file)

        # Set Audio Metadata
        self.fn = len(wf)
        self.sr = sr

        # Process Negative Audio Data
        for i in range(len(wf)):
            # Zero Negative Peaks
            if (wf[i] < 0):
                wf[i] = 0

        # Compute Minimum Audio Peak Distance
        min_dist = (sr // (1000 // PEAK_DIST))

        # Process Waveform Peaks
        return (list(scipy.signal.find_peaks(wf, distance = min_dist)[0]))

# End Class-------------------------------------------------------------------------------------------------------------------------------------------------------------
