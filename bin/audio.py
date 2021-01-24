# Developed by matthew-notaro, nalinahuja22, and ClarkChan1

import scipy
import librosa

from collections import deque

# Distance Between Audio Peaks (ms)
PEAK_DIST = 250

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
        # Load Audio File
        wf, sr = librosa.load(self.file)

        # Populate Audio Metadata
        self.frame_count = len(wf)
        self.sample_rate = sr
        self.duration = librosa.get_duration(y = wf)


    def get_audio_duration(self):
        # Audio File Duration
        return librosa.get_duration(filename=self.file)

    def get_beat_timestamps(self, start_seconds, end_seconds):
        # get data
        data, sr = librosa.load(self.afile, offset=start_seconds,duration=end_seconds-start_seconds)

        # calculate PLP sinusoid function to predict beat timestamps
        onset_env = librosa.onset.onset_strength(y=data, sr=sr)
        pulse = librosa.beat.plp(onset_envelope=onset_env, sr=sr)
        beats_plp = np.flatnonzero(librosa.util.localmax(pulse))
        time = librosa.times_like(pulse, sr=sr) + start_seconds

        # return beat timestamps
        return time[beats_plp]

    def get_peaks(self, start_seconds, end_seconds):
        # Process Negative Audio Data
        for i in range(len(wf)):
            # Zero Negative Peaks
            if (wf[i] < 0):
                wf[i] = 0

        # Compute Minimum Audio Peak Distance
        min_dist = (sr // (1000 // PEAK_DIST))

        # Process Waveform Peaks
        self.peaks = (list(scipy.signal.find_peaks(wf, distance = min_dist)[0]))


    # def plot_audio_plp():
        # # plot data
        # data, sr = librosa.load(self.afile, offset=start_seconds,duration=end_seconds-start_seconds)
        # time = (np.arange(0,len(data)) / sr) + start_seconds
        # # time = (np.arange(0,len(data)) / sr)
        # fig, ax = plt.subplots(nrows=2, sharex=True)
        # # set up plot for raw audio
        # ax[0].set(title='raw audio')
        # ax[0].plot(time, data)
        # ax[0].set(ylabel="sound amplitude")
        #
        # # set up plot for beat timestamp estimation
        # onset_env = librosa.onset.onset_strength(y=data, sr=sr)
        # pulse = librosa.beat.plp(onset_envelope=onset_env, sr=sr)
        # beats_plp = np.flatnonzero(librosa.util.localmax(pulse))
        # time = librosa.times_like(pulse, sr=sr) + start_seconds
        # # time = librosa.times_like(pulse, sr=sr)
        # ax[1].set(title='estimated beats')
        # ax[1].set(xlabel="time", ylabel="sound amplitude")
        # ax[1].plot(time, librosa.util.normalize(pulse), label='PLP')
        # ax[1].vlines(time[beats_plp], 0, 1, alpha=0.5, color='r', linestyle='--', label='PLP Beats')
        # ax[1].legend()