# Developed by Nalin Ahuja, nalinahuja22

import cli
import math
import librosa
import heapq as hp
import numpy as np

from scipy import signal
from moviepy import editor
from dataclasses import dataclass

# End Imports-----------------------------------------------------------------------------------------------------------------------------------------------------------

@dataclass
class Audio:
    # Audio File Path
    path:str

    # Audio File Object
    file:any = None

    # Audio File Metadata
    fps:int = None
    peaks:list = None
    length:float = None

@dataclass
class Peak:
    # Peak Time
    time:float

    # Peak Amplitude
    amp:float

    # Peak Sample Volume
    vol:float

    # Iterable Class View Subroutine
    def __iter__(self):
        # Return Iterable Object
        return (iter((self.time, self.amp, self.vol)))

# End Audio Classes-----------------------------------------------------------------------------------------------------------------------------------------------------

# Audio Sample Width (msec)
AUDIO_SAMPLE_WIDTH = 750

# Audio Peak Distance (msec)
AUDIO_PEAK_DISTANCE = 150

# End Audio Processing Parameters---------------------------------------------------------------------------------------------------------------------------------------

def __process_audio(audio_obj, video_obj, total_video_time):

    # Print Status
    print(cli.CR + "→ Loading {} ".format(audio_obj.path), end = "", flush = True)

    # Load Audio Frame Data With Native Sample Rate
    wf, sr = librosa.load(audio_obj.path, sr = None)

    # Absolute Audio Frame Data
    wf = np.abs(wf)

    # Set Audio File Object
    audio_obj.file = editor.AudioFileClip(audio_obj.path, fps = sr)

    # cut the audio file if it is longer than the total_video_time
    if float((audio_obj.file).duration) > total_video_time:
        print("audio file is smaller than video")
        audio_obj.file = audio_obj.file.set_duration(total_video_time)

    # Set Audio File Metadata
    audio_obj.fps = int((audio_obj.file).fps)
    audio_obj.length = float((audio_obj.file).duration)

    # Calculate Frame Sample Size
    fs = int(AUDIO_SAMPLE_WIDTH * audio_obj.fps)

    # Calculate Audio Frame Total
    ft = int(((audio_obj.fps * audio_obj.length) // fs) * fs)

    # Initalize Audio Frame Heap
    fh = []

    # Initalize Noise Floor Data List
    nf = []

    # Initalize Noise Ceiling Data List
    nc = []

    # Determine Maximum Audio Frame Index
    mwf = len(wf) - 1

    # Calculate Maximum Audio Frame Heap Size
    mfh = math.ceil(AUDIO_SAMPLE_WIDTH / AUDIO_PEAK_DISTANCE)

    # Calculate Audio Noise Data
    for i in range(0, ft, fs):
        # Print Status
        print(cli.CR + "→ Processing {} - {:.1f}% ".format(audio_obj.path, ((i / ft) * 50)), end = "", flush = True)

        # Process Audio Frame Sample
        for j in range(fs):
            # Calculate Audio Frame Index
            wfi = i + j

            # Correct Audio Frame Index
            if (wfi > mwf):
                wfi = mwf

            # Push Audio Frame
            hp.heappush(fh, wf[wfi])

            # Maintain Heap Size
            if (len(fh) > mfh):
                # Pop Audio Frame
                hp.heappop(fh)

        # Append Sample Noise Floor Value
        nf.append(np.average(wf[i:i + fs]))

        # Append Sample Noise Ceiling Value
        nc.append(np.average(fh))

        # Clear Audio Frame Heap
        fh.clear()

    # Filter Audio Frame Data
    for i in range(len(nc)):
        # Print Status
        print(cli.CR + "→ Processing {} - {:.1f}% ".format(audio_obj.path, (((i / len(nc)) * 50) + 50)), end = "", flush = True)

        # Process Audio Frame Sample
        for j in range(fs):
            # Calculate Audio Frame Index
            wfi = (i * fs) + j

            # Correct Audio Frame Index
            if (wfi > mwf):
                wfi = mwf

            # Remove Audio Data Below Noise Ceiling
            if (wf[wfi] < nc[i]):
                wf[wfi] = 0

    # Print Status
    print(cli.CR + "→ Processing {} - 100.0% ".format(audio_obj.path), end = "", flush = True)

    # Calculate Audio Peak Frame Distance
    pd = int(AUDIO_PEAK_DISTANCE * audio_obj.fps)

    # Get Audio Peak Frames
    pf, _ = signal.find_peaks(wf, distance = int(pd))

    # Normalize Audio Frame Data
    wf = np.divide(wf, np.max(wf))

    # Normalize Noise Floor Data
    nf = np.divide(nf, np.max(nf))

    # Initalize Audio Peaks List
    peaks = []

    # Determine Maximum Noise Floor Index
    mnf = len(nf) - 1

    # Iterate Over Audio Peak Frames
    for i in range(len(pf)):
        # Get Audio Peak Frame Index
        wfi = pf[i]

        # Calculate Noise Floor Index
        nfi = wfi // fs

        # Correct Noise Floor Index
        if (nfi > mnf):
            nfi = mnf

        # Append Audio Peak
        peaks.append(Peak(wfi / audio_obj.fps, wf[wfi], nf[nfi]))

    # Set Audio Peaks
    audio_obj.peaks = tuple(peaks)

    print("audio object info:")
    print("audio fps:", audio_obj.fps)
    print("audio length:", audio_obj.length)
    print("total_video_time: ", total_video_time)
    print("audio peaks:", audio_obj.peaks)
    # Print Status
    print(cli.CR + cli.CL + "→ Processed {}".format(audio_obj.path))

    # TESTING ONLY
    # import matplotlib.pyplot as plt
    # print("path: {}, fps: {}, length: {}".format(obj.path, obj.fps, obj.length))
    # for i, peak in enumerate(obj.peaks, 1):
    #     print("{} → {}".format(i, peak))
    # plt.plot(wf)
    # plt.show()

    # Return Success
    return (True)

# End Audio Processing Function-----------------------------------------------------------------------------------------------------------------------------------------

# Convert Scale To Seconds
AUDIO_SAMPLE_WIDTH /= 1000

# Convert Scale To Seconds
AUDIO_PEAK_DISTANCE /= 1000

# End Audio Module Onload Instructions----------------------------------------------------------------------------------------------------------------------------------
