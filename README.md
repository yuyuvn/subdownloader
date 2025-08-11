# Subtitle Downloader & Sync Tool

<p align="center">
  <img src="./icon/subdownloader.png" alt="tool icon" width="256"/>
</p>

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

## Windows Context Menu Integration
A sample .reg file is included to add this script to the Windows context menu (right-click inside a folder). Modify the paths in the file as needed.
