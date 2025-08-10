#!/usr/bin/env python3
import os
import sys
import subprocess
import re
from subliminal import scan_video, scan_videos, download_best_subtitles, save_subtitles
from babelfish import Language
import subliminal

def windows_path_to_wsl_path(path: str) -> str:
    # Convert Windows path like C:\path\to\file to /mnt/c/path/to/file
    m = re.match(r'^([a-zA-Z]):\\(.*)', path)
    if m:
        drive = m.group(1).lower()
        rest = m.group(2).replace('\\', '/')
        return f"/mnt/{drive}/{rest}"
    return path  # Already WSL/Linux path

def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <movie_or_folder_path> [language_code]")
        print("Example: ./sub_downloader.py '/mnt/c/Users/you/Videos' eng")
        sys.exit(1)

    input_path = windows_path_to_wsl_path(sys.argv[1])
    language_code = sys.argv[2] if len(sys.argv) > 2 else "eng"

    try:
        lang = Language(language_code)
    except ValueError:
        print(f"❌ Invalid language code: {language_code}")
        print("Examples: eng (English), vie (Vietnamese), jpn (Japanese)")
        sys.exit(1)

    if not os.path.exists(input_path):
        print(f"❌ Path not found: {input_path}")
        sys.exit(1)

    # Enable caching for subliminal
    cache_dir = os.path.expanduser('~/.cache/subdownloader')
    os.makedirs(cache_dir, exist_ok=True)
    cache_path = os.path.join(cache_dir, 'cachefile.dbm')
    subliminal.region.configure('dogpile.cache.dbm', arguments={'filename': cache_path})

    # Scan videos (single or folder)
    if os.path.isdir(input_path):
        videos = list(scan_videos(input_path))
    else:
        videos = [scan_video(input_path)]

    print(f"🔍 Found {len(videos)} video(s) to process.")

    # Download best subtitles for all videos at once
    subtitles = download_best_subtitles(videos, {lang}, providers=['opensubtitles'])

    for video in videos:
        if video in subtitles and subtitles[video]:
            best_sub = subtitles[video].pop()

            save_subtitles(video, [best_sub])
            sub_ext = getattr(best_sub, "subtitle_format", "srt")
            sub_path = os.path.splitext(video.name)[0] + f".{lang}.{sub_ext}"

            if os.path.exists(sub_path):
                print(f"✅ Downloaded: {sub_path}")

                # Sync subtitles
                print("🎯 Syncing subtitle timing with ffsubsync...")
                sync_cmd = [
                    "ffsubsync", video.name,
                    "-i", sub_path,
                    "-o", sub_path
                ]
                subprocess.run(sync_cmd, check=True)
                print(f"✅ Subtitle synced: {sub_path}")
            else:
                print(f"❌ Failed to save subtitle for {video.name}")
        else:
            print(f"❌ No subtitles found for {video.name}")

if __name__ == "__main__":
    main()
