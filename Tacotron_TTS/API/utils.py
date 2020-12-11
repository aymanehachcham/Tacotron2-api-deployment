
import os
import uuid

def get_tts_media(instance, filename):
    _, ext = os.path.splitext(filename)
    return 'tts_audio_output/{}{}'.format(uuid.uuid4(), ext)