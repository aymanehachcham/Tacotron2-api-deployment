
import os
import uuid

def get_tts_media(instance, filename):
    _, ext = os.path.splitext(filename)
    return 'ttsa_audio_output/{}{}'.format(uuid.uuid1(), ext)