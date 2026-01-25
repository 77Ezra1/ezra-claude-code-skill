# Advanced yt-dlp Features

## Playlist Downloading

```bash
# Download entire playlist
yt-dlp "PLAYLIST_URL"

# Download playlist starting from video 3
yt-dlp --playlist-start 3 "PLAYLIST_URL"

# Download only first 5 videos
yt-dlp --playlist-end 5 "PLAYLIST_URL"

# Download specific videos (1, 3, 5)
yt-dlp --playlist-items 1,3,5 "PLAYLIST_URL"

# Flat download (no playlist folders)
yt-dlp --flat-playlist "PLAYLIST_URL"
```

## Format Selection

```bash
# List all available formats
yt-dlp -F "URL"

# Download specific format by ID
yt-dlp -f 137 "URL"

# Best video + best audio (merge)
yt-dlp -f "bv+ba" "URL"

# Best single file (no merge)
yt-dlp -f "b" "URL"

# Worst quality (smallest file)
yt-dlp -f "w" "URL"

# Prefer MP4 over other formats
yt-dlp -f "bv[ext=mp4]+ba[ext=m4a]" "URL"
```

## Output Template

```bash
# Custom filename
yt-dlp -o "%(title)s.%(ext)s" "URL"

# Include upload date
yt-dlp -o "%(upload_date)s-%(title)s.%(ext)s" "URL"

# Organize by channel
yt-dlp -o "%(uploader)s/%(title)s.%(ext)s" "URL"

# Save to specific directory
yt-dlp -o "D:/Videos/%(title)s.%(ext)s" "URL"
```

## Authentication

```bash
# Username and password
yt-dlp -u username -p password "URL"

# With 2FA
yt-dlp -u username -p password --twofactor 123456 "URL"

# Video password (for password-protected videos)
yt-dlp --video-password PASSWORD "URL"

# Use cookies from browser
yt-dlp --cookies-from-browser chrome "URL"
```

## Proxy Configuration

```bash
# HTTP proxy
yt-dlp --proxy http://127.0.0.1:8080 "URL"

# SOCKS proxy
yt-dlp --proxy socks5://127.0.0.1:1080 "URL"

# Read from environment
yt-dlp --proxy "" "URL"  # Uses HTTP_PROXY env var
```

## Live Stream Recording

```bash
# Record live stream
yt-dlp "URL"

# Record with timeout (stop after 1 hour)
yt-dlp --timeout 3600 "URL"

# Retry on connection loss
yt-dlp --retries infinite "URL"

# Download live stream until manually stopped
yt-dlp --wait-for-video "URL"
```

## Speed Control

```bash
# Limit download speed (1MB/s)
yt-dlp --limit-rate 1M "URL"

# Throttle speed after 50MB downloaded
yt-dlp --limit-rate 50K --buffer-size 50K "URL"
```

## Thumbnail and Metadata

```bash
# Embed thumbnail
yt-dlp --embed-thumbnail "URL"

# Write metadata file
yt-dlp --write-info-json "URL"

# Embed metadata (requires FFmpeg)
yt-dlp --embed-metadata "URL"

# Download thumbnail only
yt-dlp --write-thumbnail --skip-download "URL"
```

## Archive and Incremental Downloads

```bash
# Track downloaded videos (don't re-download)
yt-dlp --download-archive archive.txt "URL"

# Break on existing (skip if file exists)
yt-dlp --no-overwrites "URL"

# Continue incomplete downloads
yt-dlp --continue "URL"
```

## Configuration File

Create `yt-dlp.conf` or `yt-dlp.conf.txt`:

```
# Default format
-f bestvideo+bestaudio

# Output directory
-o D:/Videos/%(title)s.%(ext)s

# Always download subtitles
--write-subs

# Embed thumbnail
--embed-thumbnail
```

Then run: `yt-dlp "URL"` (uses config file settings)
