import os
import json
import re
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from django.utils.decorators import method_decorator
import pytube
import moviepy.editor as mp

def sanitize_filename(filename):
    # Remove unsupported characters and replace spaces
    return re.sub(r'[^a-zA-Z0-9_.-]', '', filename.replace(' ', '_'))

@method_decorator(csrf_exempt, name='dispatch')
class DownloadAudioView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        youtube_url = data.get('youtube_url')
        if not youtube_url:
            return JsonResponse({'error': 'Missing YouTube URL'}, status=400)

        # Define a common parent directory for audio and video files
        parent_dir = 'media_files'
        audio_dir = os.path.join(parent_dir, 'audio')
        video_dir = os.path.join(parent_dir, 'video')

        # Create the directories if they do not exist
        os.makedirs(audio_dir, exist_ok=True)
        os.makedirs(video_dir, exist_ok=True)

        try:
            yt = pytube.YouTube(youtube_url)
            audio_stream = yt.streams.filter(only_audio=True, file_extension="mp4").first()

            safe_filename = sanitize_filename(yt.title)
            audio_filename = f"{safe_filename}.mp4"
            audio_filepath = os.path.join(video_dir, audio_filename)

            # Download the video file into the video directory
            audio_stream.download(output_path=video_dir, filename=audio_filename)

            # Define the output path for the audio file
            output_path = os.path.join(audio_dir, f"{safe_filename}.wav")

            # Convert the video file to audio
            audio_clip = mp.AudioFileClip(audio_filepath)
            audio_clip.write_audiofile(output_path, codec="pcm_s16le")
            audio_clip.close()

            # Clean up the temporary video file
            os.remove(audio_filepath)

            # Serve the audio file as a response
            with open(output_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="audio/wav")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(output_path)
                return response

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@method_decorator(csrf_exempt, name='dispatch')
class UploadAudio(View):
    def post(self, request, *args, **kwargs):
        if 'audio_file' not in request.FILES:
            return JsonResponse({'error': 'No audio file provided.'}, status=400)

        audio_file = request.FILES['audio_file']
        parent_dir = 'media_files'
        audio_dir = os.path.join(parent_dir, 'audio')
        os.makedirs(audio_dir, exist_ok=True)  # Ensure the directory exists
        file_path = os.path.join(audio_dir, audio_file.name)

        # Save the file to server
        path = default_storage.save(file_path, ContentFile(audio_file.read()))

        # Here you can add logic to process the file if needed

        return JsonResponse({'message': 'Audio file uploaded successfully.', 'path': path})