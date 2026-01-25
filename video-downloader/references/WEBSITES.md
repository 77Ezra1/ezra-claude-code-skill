# Website-Specific Patterns

## YouTube

```bash
# Basic download
yt-dlp "https://www.youtube.com/watch?v=VIDEO_ID"

# Download playlist
yt-dlp "https://www.youtube.com/playlist?list=PLAYLIST_ID"

# Download 4K video
yt-dlp -f "bestvideo[height<=2160]+bestaudio" "URL"

# Age-restricted content (use cookies)
yt-dlp --cookies-from-browser chrome "URL"

# YouTube Shorts
yt-dlp "https://youtube.com/shorts/VIDEO_ID"

# Download with chapter markers
yt-dlp --write-description --write-info-json --embed-metadata "URL"

# SponsorBlock integration (skip sponsors)
yt-dlp --sponsorblock-mark all --sponsorblock-remove all "URL"
```

## Bilibili

```bash
# Basic download
yt-dlp "https://www.bilibili.com/video/BV..."

# Download highest quality (requires login)
yt-dlp --cookies-from-browser chrome "URL"

# Download with danmaku (comments)
yt-dlp --write-subs --sub-langs ai_zh --convert-subs srt "URL"

# Download playlist
yt-dlp "https://www.bilibili.com/list/ml...

# Bilibili specific format (often FLV, needs conversion)
yt-dlp --merge-output-format mp4 "URL"

# Bangumi (anime) content
yt-dlp --cookies-from-browser chrome "https://www.bilibili.com/bangumi/play/..."
```

## Twitter / X

```bash
# Download tweet video
yt-dlp "https://twitter.com/user/status/TWEET_ID"

# Download all videos from user
yt-dlp "https://twitter.com/username"

# Download with cookies (for private accounts)
yt-dlp --cookies-from-browser chrome "URL"

# Download GIF (actually video)
yt-dlp "https://twitter.com/user/status/..."
```

## Instagram

```bash
# Download post
yt-dlp "https://www.instagram.com/p/POST_ID/"

# Download reel
yt-dlp "https://www.instagram.com/reels/REEL_ID/"

# Download story (requires login)
yt-dlp --cookies-from-browser chrome "https://www.instagram.com/stories/..."

# Download from user profile
yt-dlp "https://www.instagram.com/username/"
```

## TikTok

```bash
# Download video
yt-dlp "https://www.tiktok.com/@user/video/VIDEO_ID"

# Download without watermark
yt-dlp --embed-metadata --write-info-json "URL"

# Download from user profile
yt-dlp "https://www.tiktok.com/@username"

# Note: Watermark removal may violate ToS
```

## Twitch

```bash
# Download VOD
yt-dlp "https://www.twitch.tv/videos/VIDEO_ID"

# Download clip
yt-dlp "https://clips.twitch.tv/CLIP_ID"

# Record live stream
yt-dlp -t 01:00:00 "https://www.twitch.tv/streamer"

# With authentication (for sub-only content)
yt-dlp --username USERNAME --password PASSWORD "URL"
```

## Reddit

```bash
# Download video from Reddit
yt-dlp "https://www.reddit.com/r/SUBREDDIT/comments/POST_ID/.../"

# Download from v.redd.it directly
yt-dlp "https://v.redd.it/VIDEO_ID"
```

## Vimeo

```bash
# Basic download
yt-dlp "https://vimeo.com/VIDEO_ID"

# Password-protected video
yt-dlp --video-password PASSWORD "URL"
```

## Facebook

```bash
# Download public video
yt-dlp "https://www.facebook.com/watch?v=VIDEO_ID"

# Download with cookies for private content
yt-dlp --cookies-from-browser chrome "URL"
```

## Dailymotion

```bash
# Basic download
yt-dlp "https://www.dailymotion.com/video/VIDEO_ID"

# Download playlist
yt-dlp "https://www.dailymotion.com/playlist/..."
```

## Coursera / Udemy

```bash
# Requires authentication
yt-dlp --username EMAIL --password PASSWORD "COURSE_URL"

# Or use cookies
yt-dlp --cookies-from-browser chrome "COURSE_URL"
```

## Generic Tips

```bash
# Check if URL is supported
yt-dlp --list-extractors | grep WEBSITE_NAME

# Force specific extractor
yt-dlp --extractor-restriction "generic" "URL"

# Use generic extractor for unknown sites
yt-dlp --extractor-args "generic:force_single_product=True" "URL"

# Simulate download (test without downloading)
yt-dlp --simulate "URL"

# Get video info without downloading
yt-dlp --dump-json "URL"
```
