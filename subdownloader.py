#!/usr/bin/env python3
import os
import sys
import subprocess
import re
from subliminal import scan_video, download_best_subtitles, save_subtitles
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
        print(f"Usage: {sys.argv[0]} <movie_path> [language_code]")
        print("Example: ./sub_downloader.py '/mnt/c/Users/you/Videos/movie.mkv' eng")
        sys.exit(1)

    movie_path = windows_path_to_wsl_path(sys.argv[1])
    language_code = sys.argv[2] if len(sys.argv) > 2 else "eng"

    if not os.path.exists(movie_path):
        print(f"❌ Error: File not found: {movie_path}")
        sys.exit(1)

    try:
        lang = Language(language_code)
    except ValueError:
        print(f"❌ Invalid language code: {language_code}")
        print("Examples: eng (English), vie (Vietnamese), jpn (Japanese)")
        sys.exit(1)

    # Scan movie metadata
    video = scan_video(movie_path)

    # Enable caching for subliminal
    cache_dir = os.path.expanduser('~/.cache/subdownloader')
    os.makedirs(cache_dir, exist_ok=True)
    cache_path = os.path.join(cache_dir, 'cachefile.dbm')
    subliminal.region.configure('dogpile.cache.dbm', arguments={'filename': cache_path})

    print(f"🔍 Searching subtitles for: {video.name} ({lang})")
    subtitles = download_best_subtitles([video], {lang}, providers=['opensubtitles'])

    if video in subtitles and subtitles[video]:
        best_sub = subtitles[video].pop()

        # Save the subtitle file
        save_subtitles(video, [best_sub])

        # Determine saved file path
        sub_ext = getattr(best_sub, "subtitle_format", "srt")
        sub_path = os.path.splitext(movie_path)[0] + f".{lang}.{sub_ext}"

        if os.path.exists(sub_path):
            print(f"✅ Downloaded: {sub_path}")

            # Sync with ffsubsync
            print("🎯 Syncing subtitle timing with ffsubsync...")
            sync_cmd = [
                "ffsubsync", movie_path,
                "-i", sub_path,
                "-o", sub_path
            ]
            subprocess.run(sync_cmd, check=True)
            print(f"✅ Subtitle synced: {sub_path}")
        else:
            print("❌ Failed to save subtitle file.")
    else:
        print("❌ No subtitles found.")

if __name__ == "__main__":
    main()
