# ml_processor/urls.py
from django.urls import path
from .views import MLProcessorView

urlpatterns = [
    path('process/', MLProcessorView.as_view(), name='process'),
]
