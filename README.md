# Subtitle Downloader & Sync Tool

A Python script to **download** subtitles from [OpenSubtitles](https://www.opensubtitles.org/) and **sync** them with the video using [`ffsubsync`](https://github.com/smacke/ffsubsync).  
Works with both **Windows** and **WSL/Linux** paths.

---

## Requirements

- Python 3.7+
- `ffmpeg` and `ffprobe` in PATH
- Python packages:
  ```bash
  pip install subliminal babelfish dogpile.cache ffsubsync
  ```

## Usage
```bash
./sub_downloader.py <movie_or_folder_path> [language_code]
```

## Example
```bash
# Scan whole folder
./sub_downloader.py "/mnt/c/Users/you/Videos/" eng
# Specific file
./sub_downloader.py "C:\Users\you\Videos\anime.mkv" jpn
```
