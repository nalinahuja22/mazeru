# Developed by matthew-notaro, nalinahuja22, and ClarkChan1

import argparse

from timeline import Timeline

# End Imports----------------------------------------------------------------------------------------------------------------------------------------------------------

def main():
    # Intialize Argument Parser
    parser = argparse.ArgumentParser()

    # Add Arguments
    parser.add_argument("audio_path", help="path to audio file")
    parser.add_argument("video_path", help="path to directory that contains videos")
    parser.add_argument("output_path", help="path to where the output file will be stored")
    parser.add_argument("--min-seconds", help="minimum threshold time interval to cut", type=float)
    parser.add_argument("--max-seconds", help="maximum threshold time interval to cut", type=float)

    # Parse Arguments
    args = parser.parse_args()

    # Create Timeline
    vid_maker = Timeline(args.audio_path, args.video_path, args.output_path)

    # Setup Timeline Thresholds
    if args.min_seconds:
        vid_maker.min_cthr = args.min_seconds
    if args.max_seconds:
        vid_maker.max_cthr = args.max_seconds

    # Render Timeline
    vid_maker.render()

if __name__ == "__main__":
    main()

# End File-------------------------------------------------------------------------------------------------------------------------------------------------------------
