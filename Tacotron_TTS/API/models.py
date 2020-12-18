
import uuid
from django.db import models
from .utils import get_tts_media

# Create your models here.
class TTSSound(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text_content = models.TextField(null=True, blank=True)
    audio_join = models.FileField(upload_to=get_tts_media, null=True, blank=True)
    inference_time = models.CharField(max_length=255,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)