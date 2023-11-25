from django.urls import path
from .views import DownloadAudioView, UploadAudio

urlpatterns = [
    path('upload_video/', DownloadAudioView.as_view(), name='upload_video'),
    path('upload_audio/', UploadAudio.as_view(), name='upload_audio'),
]
