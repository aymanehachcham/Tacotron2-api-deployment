
from rest_framework import serializers
from .models import TTSSound

class TTSOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = TTSSound
        fields = ('uuid', 'text_content', 'audio_join', 'inference_time', 'created_at')