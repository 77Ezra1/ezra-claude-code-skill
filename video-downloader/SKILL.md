---
name: video-downloader
description: Video and audio downloading tool using yt-dlp and ffmpeg. Use when user asks to: download videos/audio from websites (YouTube, Bilibili, Twitter, Instagram, etc.), convert video formats, extract audio, download subtitles, process playlists, record streams, or any video/audio downloading and processing tasks. Supports 1000+ websites via yt-dlp.
user-invocable: true
---


# Video Downloader

This skill provides video/audio downloading and processing capabilities using yt-dlp and ffmpeg.

## Prerequisites

- yt-dlp must be installed
- ffmpeg must be installed

Verify installation:
```bash
yt-dlp --version
ffmpeg -version
```

## Quick Start

### Basic Video Download

Download video in best quality:
```bash
yt-dlp "URL"
```

### Download Audio Only

Extract and save as MP3:
```bash
yt-dlp -x --audio-format mp3 "URL"
```

### Download with Specific Quality

```bash
# 1080p or lower
yt-dlp -f "bestvideo[height<=1080]+bestaudio" "URL"

# 720p only
yt-dlp -f "bestvideo[height<=720]+bestaudio" "URL"
```

### Download Subtitles

```bash
# Download available subtitles
yt-dlp --write-subs --sub-langs all "URL"

# Download auto-generated subtitles
yt-dlp --write-auto-subs "URL"

# Embed subtitles in video
yt-dlp --embed-subs "URL"
```

## Advanced Features

See [ADVANCED.md](references/ADVANCED.md) for:
- Playlist downloading
- Format selection
- Authentication and cookies
- Proxy configuration
- Live stream recording
- Speed throttling

## Format Conversion

Use ffmpeg for conversions after downloading:

See [FFMPEG.md](references/FFMPEG.md) for:
- Video format conversion
- Audio extraction
- Video cropping and trimming
- Merging video and audio
- Adding watermarks
- Batch processing

## Common Website Patterns

See [WEBSITES.md](references/WEBSITES.md) for site-specific tips:
- YouTube
- Bilibili
- Twitter/X
- Instagram
- TikTok
- And more...

## Troubleshooting

See [TROUBLESHOOTING.md](references/TROUBLESHOOTING.md) for:
- Installation issues
- Network problems
- Format selection errors
- Subtitle issues
