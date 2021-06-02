# Developed by Nalin Ahuja, nalinahuja22

import cli
import cv2
import numpy as np

from scipy import signal
from moviepy import editor
from dataclasses import dataclass

# End Imports-----------------------------------------------------------------------------------------------------------------------------------------------------------

@dataclass
class Video:
    # Video File Path
    path:str

    # Video File Object
    file:any = None

    # Video File Metadata
    fps:float = None
    size:tuple = None
    scenes:list = None
    length:float = None

@dataclass
class Scene:
    # Scene Time
    time:float

    # Scene Length
    length:float

    # Scene Motion
    motion:float

    # Post Initalization Subroutine
    def __post_init__(self):
        # Relativize Scene Length
        self.length -= self.time

    # Iterable Class View Subroutine
    def __iter__(self):
        # Return Iterable Object
        return (iter((self.start, self.length, self.motion)))

# End Video Classes-----------------------------------------------------------------------------------------------------------------------------------------------------

# Frame Offset (fr)
FRAME_OFFSET = 2

# Minimum Cut Distance (msec)
MINIMUM_CUT_DISTANCE = 250

# Frame Difference Threshold (%)
FRAME_DIFFERENCE_THRESHOLD = 15

# Frame Difference Prominence (%)
FRAME_DIFFERENCE_PROMINENCE = 15

# Frame Capture Dimensions (px, px)
FRAME_CAPTURE_DIMENSIONS = (60, 33)

# Gaussian Kernel Dimensions (px, px)
GAUSSIAN_KERNEL_DIMENSIONS = (5, 5)

# End Video Processing Parameters---------------------------------------------------------------------------------------------------------------------------------------

def __process_video(obj):
    # Print Status
    print(cli.CR + "→ Loading {} ".format(obj.path), end = "", flush = True)

    # Set Video File Object
    obj.file = editor.VideoFileClip(obj.path)

    # Set Video File Metadata
    obj.fps = float((obj.file).fps)
    obj.size = tuple((obj.file).size)
    obj.length = float((obj.file).duration)

    # Create Video Stream
    stream = cv2.VideoCapture(obj.path)

    # Verify Video Stream
    if (not(stream.isOpened())):
        # Return Error
        return (False)

    # Initalize Frame Difference List
    fd = []

    # Calculate Video Frame Total
    ft = int(obj.fps * obj.length)

    # Define Previous Video Frame
    pf = None

    # Read Video Frame From Stream
    ret, fr = stream.read()

    # Process Video Frames
    while (ret):
        # Print Status
        print(cli.CR + "→ Processing {} - {:.1f}% ".format(obj.path, ((len(fd) / ft) * 95)), end = "", flush = True)

        # Resize Video Frame
        fr = cv2.resize(fr, FRAME_CAPTURE_DIMENSIONS, interpolation = cv2.INTER_AREA)

        # Remove Gaussian Noise
        fr = cv2.GaussianBlur(fr, GAUSSIAN_KERNEL_DIMENSIONS, cv2.BORDER_DEFAULT)

        # Convert Frame Colorspace To HSV
        fr = cv2.cvtColor(fr, cv2.COLOR_BGR2HSV)

        # Extract Frame HSV Data
        cf = cv2.split(fr)

        # Verify Previous Frame
        if (pf):
            # Get Current Frame HSV Components
            hc, sc, vc = cf

            # Get Previous Frame HSV Components
            hp, sp, vp = pf

            # Calculate HSV Component Differences
            hd = np.sum(np.abs(np.subtract((hc).astype(np.int32), (hp).astype(np.int32))))
            sd = np.sum(np.abs(np.subtract((sc).astype(np.int32), (sp).astype(np.int32))))
            vd = np.sum(np.abs(np.subtract((vc).astype(np.int32), (vp).astype(np.int32))))

            # Append Aggretate Interframe HSV Difference
            fd.append(hd + sd + vd)

        # Update Previous Video Frame
        pf = cf

        # Read Video Frame From Stream
        ret, fr = stream.read()

    # Print Status
    print(cli.CR + "→ Processing {} - 100.0% ".format(obj.path), end = "", flush = True)

    # Verify Frame Difference List
    if (not(len(fd))):
        # Return Error
        return (False)

    # Intialize Motion Data List
    md = np.copy(fd)

    # Normalize Frame Difference List
    fd = np.divide(fd, np.max(fd))

    # Remove Frame Differences Below Difference Threshold
    fd = np.where(fd > float(FRAME_DIFFERENCE_THRESHOLD), fd, 0)

    # Determine Video Cut Frames
    cuts, _ = signal.find_peaks(fd, prominence = float(FRAME_DIFFERENCE_PROMINENCE), distance = float(MINIMUM_CUT_DISTANCE * obj.fps), width = 1)

    # Initialize Scenes List
    scenes = []

    # Verify Cuts List
    if (len(cuts)):
        # Initalize Scene Times
        st, et = 0, float((cuts[0] - FRAME_OFFSET) / obj.fps)

        # Calculate Scene Motion Score
        ms = np.average(md[:cuts[0]])

        # Verify Scene Time Range
        if (st < et <= obj.length):
            # Append Starting Scene
            scenes.append(Scene(st, et, ms))

        # Iterate Over Intermediate Cuts
        for i in range(len(cuts) - 1):
            # Update Scene Times
            st, et = float((cuts[i] + FRAME_OFFSET) / obj.fps), float((cuts[i + 1] - FRAME_OFFSET) / obj.fps)

            # Calculate Scene Motion Score
            ms = np.average(md[cuts[i]:cuts[i + 1]])

            # Verify Scene Time Range
            if (st < et <= obj.length):
                # Append Intermediate Scene
                scenes.append(Scene(st, et, ms))

        # Update Scene Times
        st, et = float((cuts[-1] + FRAME_OFFSET) / obj.fps), obj.length

        # Calculate Scene Motion Score
        ms = np.average(md[cuts[-1]:])

        # Verify Scene Time Range
        if (st < et <= obj.length):
            # Append Ending Scene
            scenes.append(Scene(st, et, ms))
    else:
        # Initialize Scene Times
        st, et = 0, obj.length

        # Calculate Scene Motion Score
        ms = np.average(md)

        # Verify Scene Time Range
        if (st < et <= obj.length):
            # Append Entire Video As Scene
            scenes.append(Scene(st, et, ms))

    # Set Video Scenes
    obj.scenes = tuple(scenes)

    # Print Status
    print(cli.CR + cli.CL + "→ Processed {}".format(obj.path))

    # TESTING ONLY
    # import matplotlib.pyplot as plt
    # print("path: {}, size: {}, fps: {}, length: {}".format(obj.path, obj.size, obj.fps, obj.length))
    # for i, scene in enumerate(obj.scenes, 1):
    #     print("{} → {}".format(i, scene))
    # plt.plot(fd)
    # plt.show()
    print("size: ", obj.size)
    print("length: ", obj.length)
    print("scenes list: ", obj.scenes)

    # Return Success
    return (True)

# End Video Processing Function-----------------------------------------------------------------------------------------------------------------------------------------

# Convert Scale To Seconds
MINIMUM_CUT_DISTANCE /= 1000

# Convert Scale To Decimal
FRAME_DIFFERENCE_THRESHOLD /= 100

# Convert Scale To Decimal
FRAME_DIFFERENCE_PROMINENCE /= 100

# End Video Module Onload Instructions----------------------------------------------------------------------------------------------------------------------------------
