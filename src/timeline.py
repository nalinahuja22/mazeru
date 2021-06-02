# Developed by Nalin Ahuja, nalinahuja22

import os
import cli
import sys
import media
import random
import numpy as np

from moviepy import editor
from dataclasses import dataclass
from collections import defaultdict

# End Imports-----------------------------------------------------------------------------------------------------------------------------------------------------------

# Supported Audio File Formats
AUDIO_FORMATS = (".m4a", ".mp3", ".wav")

# Supported Video File Formats
VIDEO_FORMATS = (".avi", ".mp4", ".mov")

# Render Aspect Ratio (dec)
RENDER_ASPECT_RATIO = 1.78

# Minimum Cut Length (sec)
MINIMUM_CUT_LENGTH = 0.75

# Average Cut Length (sec)
AVERAGE_CUT_LENGTH = 2.00

# Average Cut Variation (sec)
AVERAGE_CUT_VARIATION = 0.75

# End Rendering Constants-----------------------------------------------------------------------------------------------------------------------------------------------

@dataclass
class Clip:
    # Video File Object
    file:any

    # Clip Time
    time:float = None

    # Clip Length
    length:float = None

    # Clip Motion
    motion:float = 0

    # Iterable Class View Subroutine
    def __iter__(self):
        # Return Iterable Object
        return (iter((self.file, self.time, self.length, self.motion)))

    # File Clip Creation Function
    def create(self):
        # Return Created Video Clip
        return ((self.file).subclip(self.time, self.time + self.length))

class Sequence:
    # Class Intalization Subroutine
    def __init__(self):
        # Clip Sequence
        self.clips = []

        # Clip Sequence Length
        self.length = 0

    # Class Field Length Subroutine
    def __len__(self):
        # Return Clip Sequence Length
        return (len(self.clips))

    # Clip Sequence Modifier Function
    def add(self, clip):
        # Add Clip To Sequence
        (self.clips).append(clip)

        # Update Sequence Length
        self.length += clip.duration

# End Supporting Data Classes-------------------------------------------------------------------------------------------------------------------------------------------

class Timeline:
    def __init__(self, args):
        # Seed Random Module
        random.seed(os.urandom(1024))

        # Initialize Media Paths
        self.audio_path = str(args.audio_path)
        self.video_path = str(args.video_path)
        self.output_path = str(args.output_path)

        # Define Media Objects
        self.audio_obj = None
        self.video_obj = []
        self.total_video_time = 0
        self.combined_video = None

        # Import Media
        self.import_media()

        # Process Media
        self.process_media()
        # print("length of self.combined_video: ", float(self.combined_video.duration))

        # Set Preferences
        self.set_prefs(args)

        # Export Media
        # self.export_media()

    def set_prefs(self, args):
        # Initialize Minimum Cut Length Preference
        self.minimum_cut = MINIMUM_CUT_LENGTH

        # Override Minimum Cut Length
        if ((args.minimum_cut) and (args.minimum_cut > MINIMUM_CUT_LENGTH)):
            self.minimum_cut = float(args.minimum_cut)

        # Initialize Average Cut Length Preference
        self.average_cut = AVERAGE_CUT_LENGTH

        # Override Average Cut Length
        if ((args.average_cut) and (args.average_cut >= self.minimum_cut)):
            self.average_cut = float(args.average_cut)

        # Initialize Average Cut Variation Preference
        self.cut_variation = AVERAGE_CUT_VARIATION

        # Override Average Cut Variation
        if ((args.cut_variety) and ((self.average_cut - args.cut_variety) >= self.minimum_cut)):
            self.cut_variation = float(args.cut_variety)

        # Initialize Skip Video Preference
        self.skip_video = False

        # Override Skip Video
        if (args.skip_video):
            self.skip_video = bool(args.skip_video)

        # Initialize Match Video Preference
        self.match_video = False

        # Override Average Cut
        if (args.match_video):
            self.match_video = bool(args.match_video)

        # Initialize Retain Order Preference
        self.retain_order = False

        # Override Average Cut
        if (args.retain_order):
            self.retain_order = bool(args.retain_order)

        # Initialize Video Size Preference
        self.size = min(self.video_obj, key = lambda obj : obj.size[1]).size

        # Override Video Dimension
        if ((args.resolution) and (0 < args.resolution <= self.size[1])):
            self.size = (int(args.resolution) * RENDER_ASPECT_RATIO, int(args.resolution))

        # Initialize Video Frame Rate Preference
        self.video_fps = min(self.video_obj, key = lambda obj : obj.fps).fps

        # Override Video Frame Rate
        if ((args.frame_rate) and (0 < args.frame_rate <= self.video_fps)):
            self.video_fps = float(args.frame_rate)

        # Initialize Audio Sample Rate Preference
        self.audio_fps = int((self.audio_obj).fps)

        # Override Audio Sample Rate
        if ((args.sample_rate) and (0 < args.sample_rate <= self.audio_fps)):
            self.audio_fps = int(args.sample_rate)

        # Initialize Render Thread Count Preference
        self.num_threads = 1

        # Override Render Thread Count
        if ((args.num_threads) and (args.num_threads > 0)):
            self.num_threads = int(args.num_threads)

    def import_media(self):
        # Print Status
        print("mazeru: Importing media...", end = "", flush = True)

        # process video
        # Check Path Type
        if (os.path.isfile(self.video_path)):
            # Check Video File Extension
            if (((self.video_path).lower()).endswith(VIDEO_FORMATS)):
                # Import Video File
                (self.video_obj).append(media.Video(self.video_path))
            else:
                # Get File Extension
                _, ext = os.path.splitext(self.video_path)

                # Exit Program
                sys.exit(cli.CR + "mazeru: Unsupported video format \"{}\" encountered during import, exiting...".format(ext))
        else:
            # Get List Of Video Files
            files = sorted(os.listdir(self.video_path))

            # Iterate Over Video Files
            for file in (files):
                # Check Video File Extension
                if ((file.lower()).endswith(VIDEO_FORMATS)):
                    # Import Video File
                    (self.video_obj).append(media.Video(os.path.join(self.video_path, file)))

            # Check Video Object List
            if (not(len(self.video_obj))):
                # Exit Program
                sys.exit(cli.CR + "mazeru: No supported footage found, exiting...")

        # process audio
        # Check Audio File Extension
        if (((self.audio_path).lower()).endswith(AUDIO_FORMATS)):
            # Import Audio File
            self.audio_obj = media.Audio(self.audio_path)
        else:
            # Get File Extension
            _, ext = os.path.splitext(self.audio_path)

            # Exit Program
            sys.exit(cli.CR + "mazeru: Unsupported audio format \"{}\" encountered during import, exiting...".format(str(ext)))

        # Print Status
        print(cli.CR + cli.CL + "mazeru: Imported media", flush = True)

    def process_media(self):

        # Print Status
        print("mazeru: Processing video...", flush = True)

        # Process Video Media
        # create a list of VideoFileClips
        videos = []
        # loop over all video objects and create VideoFileClips and concatenate them together
        for obj in (self.video_obj):
            # create VideoFileClip
            video = editor.VideoFileClip(obj.path)
            # concatenate it to the list
            videos.append(video)
            # increment total video time
            self.total_video_time += float(video.duration)
            # still process the video object so the preferences can be set
            media.process(obj)
        # for obj in (self.video_obj):
        #     # Process Video Object
        #     media.process(obj)
        #     self.total_video_time += obj.length

        # concatenate all the videos together
        self.combined_video = editor.concatenate_videoclips(videos)

        # Clear Outputs
        cli.cl(len(self.video_obj) + 1)

        # Print Status
        print(cli.CR + "mazeru: Processed video", flush = True)

        # Print Status
        print("mazeru: Processing audio...", flush = True)

        # Process Audio Media
        media.process(self.audio_obj, self.video_obj, self.total_video_time)

        # Clear Outputs
        cli.cl(2)

        # Print Status
        print(cli.CR + "mazeru: Processed audio", flush = True)

    def export_media(self):
        # Print Status
        print(cli.CR + "mazeru: Generating clip sequence...", end = "", flush = True)

        # Initalize Groups Dictionary
        groups = defaultdict(list)

        # Iterate Over Audio Peaks
        for peak in ((self.audio_obj).peaks):
            # Group Peaks By Minimum Cut Length
            groups[peak.time // MINIMUM_CUT_LENGTH].append(peak)

        # Initalize Audio Peaks List
        peaks = []

        # Iterate Over Peak Groups
        for key in sorted(groups.keys()):
            # Append Audio Peak In Group By Maximum Amplitude
            peaks.append(max(groups[key], key = lambda peak : peak.amp))

        # Initalize Selected Peaks List
        sel_peaks = [peaks[0]]

        # Iterate Over Audio Peaks
        for i in range(1, len(peaks)):
            # Get Current Peak
            curr_peak = peaks[i]

            # Get Previous Selected Peak
            prev_peak = sel_peaks[-1]

            # Verify Audio Peak Separation Satisfies Minimum Cut Length
            if ((curr_peak.time - prev_peak.time) < MINIMUM_CUT_LENGTH):
                # Skip Audio Peak
                continue

            # Append Peak To Selected Peaks List
            sel_peaks.append(curr_peak)

        # Update Peaks List
        peaks = sel_peaks

        # Initalize Clips List
        clips = []

        # Iterate Over Video Objects
        for video in (self.video_obj):
            # Initalize Clip Object
            clip = Clip(video.file)

            # Initalize Clip Motion List
            clip_motion = []

            # Iterate Over Scenes
            for i, scene in enumerate(video.scenes, 1):
                # Determine Clip Action
                if (clip.time is None):
                    # Set Clip Object Time
                    clip.time = scene.time

                    # Set Clip Object Length
                    clip.length = scene.length

                # Add Clip Motion Data To List
                clip_motion.append((scene.motion, scene.length))

                # Set Clip Length
                clip.length = scene.time + scene.length - clip.time

                # Verify Clip Length Satisfies Minimum Cut Length
                if ((clip.length < self.minimum_cut) and (i < len(video.scenes))):
                    # Skip Scene
                    continue

                # Unzip Clip Motion List
                motion_scores, clip_weights = list(zip(*clip_motion))

                # Clear Clip Motion List
                clip_motion.clear()

                # Set Clip Object Motion
                clip.motion = np.average(motion_scores, weights = clip_weights)

                # Append Clip Object To Clips List
                clips.append(clip)

                # Reset Clip Object
                clip = Clip(video.file)

        # Get Motion Scores From All Clips
        motion_scores = [clip.motion for clip in (clips)]

        # Normalize Motion Scores
        motion_scores = np.divide(motion_scores, np.max(motion_scores))

        # Iterate Over Motion Scores
        for i, motion_score in enumerate(motion_scores):
            # Assign Normalized Motion Score To Corresponding Clip
            clips[i].motion = motion_score

        # Check For Order Option
        if (not(self.retain_order)):
            # Sort Clips By Length
            clips.sort(key = lambda clip : clip.length)

        # Deallocate Video Objects List
        self.video_obj = None

        # Initialize Clip Sequence
        seq = Sequence()

        # Initialize Previous Peak
        prev_peak = 0

        # Initalize Clips Remaining
        clips_rem = len(clips)

        # Iterate Over Peaks
        for curr_peak in (peaks):
            # Check For Remaining Clips
            if (not(clips_rem)):
                # Break Peak Loop
                break

            # Calculate Cut Length
            cut_length = curr_peak.time - prev_peak

            # Verify Minimum Cut Length
            if (cut_length < self.minimum_cut):
                # Skip Audio Peak
                continue

            # Select Clip From List
            if ((self.average_cut - (self.cut_variation * random.random() * 0.65)) < ((cut_length + seq.length) / (len(seq) + 1))):
                # Define Selected Clip
                sel_clip = None

                # Iterate Over Clip List
                for i in range(0, len(clips), 1):
                    # Get Clip From List
                    clip = clips[i]

                    # Verify Clip
                    if (not(clip)):
                        # Skip Clip
                        continue

                    # Verify Clip Duration
                    if (clip.length < cut_length):
                        # Skip Clip
                        continue

                    # Update Clip Length
                    clip.length = cut_length

                    # Initialize Selected Clip
                    sel_clip = clip.create()

                    # Update Clips Remaining
                    clips_rem -= 1

                    # Mark Clip As Used
                    clips[i] = None

                    # Break Clip Loop
                    break

                # Verify Selected Clip
                if (not(sel_clip)):
                    # Initialize Clip Subsequence
                    sub_seq = Sequence()

                    # Iterate Over Clip List
                    for i in range(len(clips) - 1, 0, -1):
                        # Get Clip From List
                        clip = clips[i]

                        # Verify Clip
                        if (not(clip)):
                            # Skip Clip
                            continue

                        # Verify Subsequence Length
                        if (sub_seq.length >= cut_length):
                            # Break Clip Loop
                            break

                        # Add Clip To Subsequence
                        sub_seq.add(clip.file)

                        # Update Clips Remaining
                        clips_rem -= 1

                        # Mark Clip As Used
                        clips[i] = None

                    # Verify Clip Subsequence Length
                    if (sub_seq.length >= cut_length):
                        # Concatenate Clip Subsequence
                        sub_seq = editor.concatenate_videoclips(sub_seq.clips)

                        # Update Clip Length
                        sub_seq.length = cut_length

                        # Initialize Selected Clip
                        sel_clip = sub_seq.create()

                # Verify Selected Clip
                if (not(sel_clip)):
                    # Break Audio Loop
                    break

                # Append Clip To Sequence
                seq.add(sel_clip)

                # Update Previous Peak
                prev_peak = curr_peak.time

        # Verify Clip Sequence
        if (not(len(seq.clips))):
            # Exit Program
            sys.exit(cli.CR + "mazeru: Clip sequence is empty, exiting...")

        # Print Status
        print(cli.CR + cli.CL + "mazeru: Exporting media...", flush = True)

        # Concatenate Clip Sequence
        render = editor.concatenate_videoclips(seq.clips)

        # Set Render Video Dimensions
        render = render.resize(width = self.size[0], height = self.size[1])

        # Set Render Audio Source
        render = render.set_audio((self.audio_obj).file)

        # Set Sequence Duration
        render = render.subclip(0, seq.length)

        # Get Terminal Size
        width, _ = cli.size()

        # Print Separator
        print(cli.NL + ("-" * int(width)) + cli.NL)

        # Get Export Confirmation
        confirm = cli.prompt("mazeru: Confirm export ({}m{}s, {}fps, {}hz) [y/n]: ".format(int(render.duration / 60),
                                                                                           int(render.duration % 60),
                                                                                           int(self.video_fps),
                                                                                           int(self.audio_fps)))

        # Verify Confirmation
        if (not(confirm.lower() == "y")):
            # Print Separator
            print(cli.NL + ("-" * int(width)))

            # Print Status
            print(cli.NL + "mazeru: Export aborted, exiting..." + cli.NL, flush = True)
        else:
            # Print Separator
            print(cli.NL, end = "")

            # Determine Output Video Directory
            d_name = str(os.path.dirname(self.output_path))

            # Determine Output Video Basename
            v_name = str((os.path.basename(self.output_path).split("."))[0])

            # Create Output Audio Basename
            a_name = str(os.path.join(d_name, "{}_audio.mp4".format(v_name)))

            # Render Sequence As Video
            render.write_videofile(self.output_path, fps = self.video_fps, audio_fps = self.audio_fps, threads = self.num_threads, temp_audiofile = a_name)

            # Print Separator
            print(cli.NL + ("-" * int(width)))

            # Print Status
            print(cli.NL + "mazeru: Exported video to {}".format(self.output_path) + cli.NL, flush = True)

# End Timeline Class----------------------------------------------------------------------------------------------------------------------------------------------------
