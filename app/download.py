
import pytube
import moviepy.editor as mp


def download_audio(youtube_url, output_path):
    yt = pytube.YouTube(youtube_url)
    audio_stream = yt.streams.filter(only_audio=True, file_extension="mp4").first()
    audio_stream.download(filename="temp_audio.mp4")
    audio_clip = mp.AudioFileClip("temp_audio.mp4")
    audio_clip.write_audiofile(output_path, codec="pcm_s16le")
    audio_clip.close()

# usage: download_audio(youtube_url, output_path)