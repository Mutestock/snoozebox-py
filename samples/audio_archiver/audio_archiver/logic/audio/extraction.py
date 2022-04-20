from __future__ import unicode_literals
from youtube_dl import YoutubeDL
from youtube_dl.utils import ExtractorError, DownloadError
from utils.config import CONFIG


class YtLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


ydl_opts: dict = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': f"{CONFIG['audio_output_folder']}/%(title)-s/%(channel)s.%(ext)s",
    'logger': YtLogger(),
    'progress_hooks': [my_hook],
}

def get_yt_video_info(url: str) -> dict:
    try:
        with YoutubeDL(ydl_opts) as ydl:
            return ydl.extract_info(url, download=False)
    except (ExtractorError, DownloadError) as e:
        return {"status": "unavailable"}
    except Exception as e:
        print("Shit happened: ")
        print(e)
        return {"status": "server error"}
        

def download_yt_video(url: str):
    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download(url)
    except Exception as e:
        print(e)
    

