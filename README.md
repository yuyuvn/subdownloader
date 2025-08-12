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
  pip install -r requirements.txt
  ```

## Usage
### CLI
```bash
./sub_downloader.py <movie_or_folder_path> [language_code]
```

### Web
```bash
BASE_PATH=/mnt/c/Users/you/Videos DEFAULT_LANG=eng web.py
```

### Docker
```bash
docker build . -t subdownloader:latest
docker run --rm -it subdownloader:latest -e BASE_PATH=/movies -e DEFAULT_LANG=eng -e SECRET_KEY=random_secret_key SESSION_FILE_DIR=/tmp -p 5000:5000 -v /mnt/c/Users/you/Videos:/movies
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
