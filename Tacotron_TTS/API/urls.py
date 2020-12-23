from django.urls import path
from django.conf.urls.static import static
from . import views
from django.conf import settings



app_name = 'API'

urlpatterns = [
    path(r'test', views.test_api, name='test_api_communication'),
    path(r'tts/', views.tts_transcription),
    path(r'clean', views.empty_folder)

]