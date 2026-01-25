# FFmpeg Video/Audio Processing

## Basic Conversion

```bash
# Convert MP4 to MKV
ffmpeg -i input.mp4 output.mkv

# Convert to MP4 (H.264 + AAC)
ffmpeg -i input.avi -c:v libx264 -c:a aac output.mp4

# Convert WebM to MP4
ffmpeg -i input.webm -c:v libx264 -c:a aac output.mp4
```

## Extract Audio

```bash
# Extract audio as MP3
ffmpeg -i video.mp4 -vn -acodec libmp3lame -q:a 2 audio.mp3

# Extract as AAC
ffmpeg -i video.mp4 -vn -acodec aac audio.aac

# Extract as WAV (lossless)
ffmpeg -i video.mp4 -vn audio.wav
```

## Video Quality Control

```bash
# Constant Rate Factor (CRF) - lower = better quality (0-51, default 23)
ffmpeg -i input.mp4 -crf 20 output.mp4

# Two-pass encoding for precise bitrate
ffmpeg -i input.mp4 -b:v 2M -pass 1 -f mp4 /dev/null
ffmpeg -i input.mp4 -b:v 2M -pass 2 output.mp4

# Scale resolution (720p)
ffmpeg -i input.mp4 -vf scale=-1:720 output.mp4

# Scale to specific width (maintain aspect ratio)
ffmpeg -i input.mp4 -vf scale=1280:-1 output.mp4
```

## Trim Video

```bash
# Trim from 00:01:00 to 00:02:00
ffmpeg -i input.mp4 -ss 00:01:00 -to 00:02:00 -c copy output.mp4

# Trim first 30 seconds
ffmpeg -i input.mp4 -t 30 -c copy output.mp4

# Trim using fast seek (less accurate but faster)
ffmpeg -ss 00:01:00 -i input.mp4 -to 00:02:00 -c copy output.mp4
```

## Merge Videos

```bash
# Concatenate using file list
# Create file.txt with:
# file 'video1.mp4'
# file 'video2.mp4'

ffmpeg -f concat -safe 0 -i file.txt -c copy output.mp4

# Merge video and audio
ffmpeg -i video.mp4 -i audio.mp3 -c:v copy -c:a aac output.mp4
```

## Rotate/Flip Video

```bash
# Rotate 90 degrees clockwise
ffmpeg -i input.mp4 -vf "transpose=1" output.mp4

# Rotate 90 degrees counter-clockwise
ffmpeg -i input.mp4 -vf "transpose=2" output.mp4

# Flip horizontally
ffmpeg -i input.mp4 -vf "hflip" output.mp4

# Flip vertically
ffmpeg -i input.mp4 -vf "vflip" output.mp4
```

## Add Watermark

```bash
# Add image watermark at top-left
ffmpeg -i input.mp4 -i watermark.png -filter_complex "overlay=10:10" output.mp4

# Add watermark at bottom-right
ffmpeg -i input.mp4 -i watermark.png -filter_complex "overlay=W-w-10:H-h-10" output.mp4

# Add text watermark
ffmpeg -i input.mp4 -vf "drawtext=text='Watermark':fontsize=24:fontcolor=white:x=10:y=10" output.mp4
```

## Extract Frames

```bash
# Extract one frame per second
ffmpeg -i input.mp4 -r 1 frame_%04d.png

# Extract frame at specific timestamp
ffmpeg -ss 00:00:10 -i input.mp4 -frames:v 1 frame.jpg

# Extract frames as thumbnails (every 5 seconds)
ffmpeg -i input.mp4 -vf "select=not(mod(n\,300))" -vsync 0 frame_%04d.png
```

## Create Video from Images

```bash
# Create video from images (10 fps)
ffmpeg -r 10 -i frame_%04d.png -c:v libx264 output.mp4

# Create slideshow (5 seconds per image)
ffmpeg -r 1/5 -i img%d.jpg -c:v libx264 output.mp4
```

## Audio Processing

```bash
# Adjust volume (increase by 2x)
ffmpeg -i input.mp4 -filter:a "volume=2.0" output.mp4

# Normalize audio
ffmpeg -i input.mp4 -filter:a "loudnorm" output.mp4

# Remove audio
ffmpeg -i input.mp4 -an output.mp4

# Mute specific section
ffmpeg -i input.mp4 -af "volume=enable='between(t,10,20)':volume=0" output.mp4
```

## Speed Up/Slow Down

```bash
# Speed up 2x
ffmpeg -i input.mp4 -filter:v "setpts=0.5*PTS" output.mp4

# Slow down to half speed
ffmpeg -i input.mp4 -filter:v "setpts=2.0*PTS" output.mp4

# Speed up audio too
ffmpeg -i input.mp4 -filter:v "setpts=0.5*PTS" -filter:a "atempo=2.0" output.mp4
```

## Crop Video

```bash
# Crop 640x360 from top-left
ffmpeg -i input.mp4 -vf "crop=640:360:0:0" output.mp4

# Crop center
ffmpeg -i input.mp4 -vf "crop=640:360:(in_w-640)/2:(in_h-360)/2" output.mp4
```

## Extract Subtitle Streams

```bash
# List all streams
ffmpeg -i input.mp4 -map 0 -dump -f null -

# Extract subtitle
ffmpeg -i input.mp4 -map 0:s:0 subs.srt

# Embed subtitle into video
ffmpeg -i input.mp4 -i subs.srt -c copy -c:s mov_text output.mp4
```

## Common Presets

```bash
# High quality MKV (H.265)
ffmpeg -i input.mp4 -c:v libx265 -crf 20 -c:a aac output.mkv

# Web optimized MP4 (fast start)
ffmpeg -i input.mp4 -movflags +faststart output.mp4

# GIF from video (first 5 seconds, 10 fps)
ffmpeg -i input.mp4 -t 5 -r 10 output.gif

# Video for Instagram (square, 1080x1080)
ffmpeg -i input.mp4 -vf "scale=1080:1080:force_original_aspect_ratio=decrease,pad=1080:1080:(ow-iw)/2:(oh-ih)/2" output.mp4
```
