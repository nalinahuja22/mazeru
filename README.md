# Mazeru (混ぜる)

Ever wanted to make aesthetic video compilations to some "Lofi hip hop mix - Beats to Relax/Study to" but didn't know where to start? Mazeru takes all the work out of editing and splices clips together along to the beat of your favorite song!

## Inspiration

Birthed out of the idea of making an auto-video editing program for car compilations, Mazeru began to take form after we expanded its initial function to the limits of the user's imagination.

## What it does

Mazeru takes a song and a collection of video clips as input and fully renders a complete compilation to the beat of the song. 

## How we built it

Mazeru was built with Python, primarily relying on the moviepy, librosa, and imagehash libraries. Moviepy was used for all the video and audio editing and splicing, librosa for the audio analysis, and imagehash for the video analysis.

## Challenges we ran into

We planned to implement a maximum video clip length threshold; however, we quickly realized that implementing such functionality would be rather complex in such a short period of time. Doing so would require another round of audio processing to extract more peaks from the audio file in the given time frame to find more potential peaks.

## Accomplishments that we're proud of

We are proud of the entire project. Managing to coordinate all necessary tasks and finishing all last minute debugging climaxed in a crescendo of both audio and video synchrony. 

## What we learned

We came to foster a fond appreciation of moviepy and learned a great deal of perseverance. After many rounds of our rendered videos coming out audio-less due to typos and

## What's next for Mazeru (混ぜる)

As for audio processing, we plan to fully implement a high-pass filter to ignore lower peaks during periods of relatively quieter sections of the given song.

As for video processing, we plan to allow for Mazeru itself to splice longer videos into shorter segments broken up by scene changes. We also plan on incorporating auto-resolution-formatting so that each video will be downscaled to the lowest shared resolution.

We will also add a title slide at the end of each video produced by Mazeru if desired.
