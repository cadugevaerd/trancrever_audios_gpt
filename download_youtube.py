import os
from pydub import AudioSegment
from pytube import YouTube
from pytube.exceptions import PytubeError
from pytube.cli import on_progress
from io import BytesIO

def download_youtube(url):
    """
    Download audio from a YouTube video and save it as an mp3 file.

    Args:
    - URL: str, the URL of the YouTube video
    - on_progress: function, a callback function to track the download progress

    Returns:
    - True if the download is successful
    - None if there is an error
    """
    try:
        yt = YouTube(url,on_progress_callback=on_progress)
        audio = yt.streams.filter(only_audio=True).first()
        out_file = audio.download()
        audio = AudioSegment.from_file(out_file)
        new_file = BytesIO()
        new_file.name = "audio.mp3"
        audio.export(new_file, format="mp3")
        os.remove(out_file)
        return new_file
    except PytubeError as yterror:
        print("error - {}".format(yterror))
        return None
    except Exception as e:
        print(print("error - {}".format(e)))
        return None