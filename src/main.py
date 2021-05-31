# Developed by Nalin Ahuja, nalinahuja22

import os
import cli
import sys
import argparse

# End Imports------------------------------------------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    # Intialize Argument Parser
    parser = argparse.ArgumentParser()

    # Media Path Arguments
    parser.add_argument("audio_path", help = "path to input audio file", type = str)
    parser.add_argument("video_path", help = "path to input video file or directory", type = str)
    parser.add_argument("output_path", help = "path to processed output video file", type = str)

    # Media Processing Arguments
    parser.add_argument("--cut-variety", help = "output video cut variety (sec)", type = float)
    parser.add_argument("--minimum-cut", help = "output video minimum cut duration (sec)", type = float)
    parser.add_argument("--average-cut", help = "output video average cut duration (sec)", type = float)

    # Media Processing Options
    parser.add_argument("--skip-video", help = "skip processing of input video files", action = "store_true")
    parser.add_argument("--match-video", help = "match output video to input audio duration", action = "store_true")
    parser.add_argument("--retain-order", help = "retain scene ordering of input video files", action = "store_true")

    # Media Rendering Arguments
    parser.add_argument("--resolution", help = "output video resolution (px)", type = int)
    parser.add_argument("--frame-rate", help = "output video frame rate (fps)", type = float)
    parser.add_argument("--sample-rate", help = "output audio sample rate (hz)", type = int)
    parser.add_argument("--num-threads", help = "number of render threads (int)", type = int)

    # Parse Arguments
    args = parser.parse_args()

    # Verify Required Media Path Arguments
    if (not(os.path.isfile(args.audio_path))):
        # Exit Program
        sys.exit("mazeru: Audio path \"{}\" is invalid, exiting...".format(args.audio_path))
    elif (not(os.path.exists(args.video_path))):
        # Exit Program
        sys.exit("mazeru: Video path \"{}\" is invalid, exiting...".format(args.video_path))
    elif (os.path.exists(args.output_path)):
        # Get Output File Overwrite Confirmation
        confirm = cli.prompt("mazeru: Output file \"{}\" exists, confirm overwrite [y/n]: ".format(args.output_path))

        # Verify Confirmation
        if (not(confirm.lower() == "y")):
            # Exit Program
            sys.exit()

    # Run Program
    try:
        # Import Timeline Class
        from timeline import Timeline

        # Create Timeline
        Timeline(args)
    except ImportError:
        # Print Status
        print(cli.nl(2) + "mazeru: Failed to create timeline, exiting...")
    except KeyboardInterrupt:
        # Print Status
        print(cli.nl(2) + "mazeru: Program interrupted by user, exiting...")
    except Exception as e:
        # Print Status
        print(cli.nl(2) + "mazeru: An unrecoverable error has occurred")

        # Print Error
        print(e)

# End Main Function------------------------------------------------------------------------------------------------------------------------------------------------------
