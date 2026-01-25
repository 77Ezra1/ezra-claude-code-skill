# Troubleshooting Guide

## Installation Issues

### yt-dlp not found

```bash
# Install via pip
pip install -U yt-dlp

# Or download standalone binary
# Windows: Download from https://github.com/yt-dlp/yt-dlp/releases
# Place in PATH or use full path

# Verify installation
yt-dlp --version
```

### ffmpeg not found

```bash
# Windows (using winget)
winget install ffmpeg

# Windows (using chocolatey)
choco install ffmpeg

# Or download manually
# https://ffmpeg.org/download.html

# Verify installation
ffmpeg -version
```

### Python not in PATH

```bash
# Find Python location
where python

# Add to PATH (Windows)
# 1. Search "Environment Variables"
# 2. Edit PATH
# 3. Add Python directory and Scripts directory
```

## Network Problems

### Connection timeout

```bash
# Increase timeout
yt-dlp --socket-timeout 60 "URL"

# Use proxy
yt-dlp --proxy http://127.0.0.1:8080 "URL"

# Retry on failure
yt-dlp --retries 10 "URL"
```

### Slow download speed

```bash
# Use aria2c for faster downloads
yt-dlp --external-downloader aria2c --external-downloader-args "-x 8 -k 2M" "URL"

# Limit speed if ISP throttles
yt-dlp --limit-rate 1M "URL"
```

### SSL/Certificate errors

```bash
# Disable certificate verification (not recommended)
yt-dlp --no-check-certificates "URL"

# Update certificates
# Windows: Update Windows
# Or use wget to download
yt-dlp --no-warnings "URL"
```

## Format Selection Issues

### Video/Audio not merging

```bash
# Specify merge format
yt-dlp --merge-output-format mp4 "URL"

# Use ffmpeg to merge manually
yt-dlp -f "bv+ba" --keep-video "URL"
ffmpeg -i video.mp4 -i audio.m4a -c copy output.mp4
```

### Format not available

```bash
# List available formats
yt-dlp -F "URL"

# Use next best format
yt-dlp -f "bestvideo*+bestaudio/best" "URL"

# Download single file only
yt-dlp -f "b" "URL"
```

### 4K/1080p not available

```bash
# Some sites require login for high quality
yt-dlp --cookies-from-browser chrome "URL"

# Or use username/password
yt-dlp -u USERNAME -p PASSWORD "URL"

# Check max available quality
yt-dlp -F "URL" | grep "height"
```

## Subtitle Issues

### Subtitles not downloading

```bash
# List available subtitles
yt-dlp --list-subs "URL"

# Download auto-generated subs
yt-dlp --write-auto-subs "URL"

# Force specific language
yt-dlp --sub-langs en,en-US "URL"

# Convert subs format
yt-dlp --convert-subs srt "URL"
```

### Subtitles out of sync

```bash
# Download video without embedded subs
yt-dlp --write-subs --skip-download "URL"

# Manually adjust using ffmpeg
ffmpeg -i video.mp4 -itsoffset 2.0 -i subs.srt -c copy -map 0:0 -map 1:0 output.mp4
```

## Site-Specific Issues

### YouTube age restriction

```bash
# Method 1: Use cookies
yt-dlp --cookies-from-browser chrome "URL"

# Method 2: Use YouTube Music
yt-dlp --extractor-args "youtube:player_client=android" "URL"

# Method 3: Use age-gate bypass
yt-dlp --extractor-args "youtube:player_client=android_embedded" "URL"
```

### Bilibili requires login

```bash
# Use cookies
yt-dlp --cookies-from-browser chrome "URL"

# Export cookies to file
# 1. Use browser extension to export cookies
# 2. Use cookie file
yt-dlp --cookies cookies.txt "URL"
```

### Private/Deleted videos

```bash
# Check Wayback Machine
# Use --get-url to see if video exists
yt-dlp --get-url "URL"

# Try archive.org
yt-dlp --proxy "" "URL"
```

## Conversion Issues

### FFmpeg codecs not available

```bash
# Check available codecs
ffmpeg -codecs

# Install full FFmpeg build
# Windows: Download from https://www.gyan.dev/ffmpeg/builds/

# Reinstall with all codecs
# Use chocolatey or full build
```

### Video/audio out of sync

```bash
# Re-encode instead of copy
ffmpeg -i input.mp4 -c:v libx264 -c:a aac output.mp4

# Fix audio delay
ffmpeg -i input.mp4 -af "adelay=500|500" output.mp4
```

## General Errors

### "HTTP Error 404: Not Found"

```bash
# Video might be deleted or region-locked
# Try proxy from different region
yt-dlp --proxy socks5://PROXY_IP:PORT "URL"
```

### "Sign in to confirm you're not a bot"

```bash
# Use cookies from browser
yt-dlp --cookies-from-browser chrome "URL"

# Or wait and retry
yt-dlp --sleep-interval 60 "URL"
```

### "Video unavailable"

```bash
# Try different extractor
yt-dlp --extractor-restriction "generic" "URL"

# Check if video is private/deleted
yt-dlp --get-url "URL"

# Use incognito cookies
yt-dlp --cookies-from-browser chrome --cookies-from-browser firefox "URL"
```

## Debug Mode

```bash
# Enable verbose output
yt-dlp -v "URL"

# Print traffic
yt-dlp --print-traffic "URL"

# Dump pages (for debugging)
yt-dlp --dump-pages "URL"

# Write debug log
yt-dlp --verbose "URL" > debug.log 2>&1
```

## Update Issues

```bash
# Update yt-dlp
pip install -U yt-dlp

# Or using yt-dlp itself
yt-dlp -U

# Windows standalone
yt-dlp --update

# Check version
yt-dlp --version
```
