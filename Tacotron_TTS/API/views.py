

from django.views.decorators.cache import never_cache
from rest_framework.response import Response
from rest_framework.decorators import api_view
from Models.handler import TacotronHandler
from .models import TTSSound
from rest_framework import status
from .serializers import TTSOutputSerializer
import os
import shutil

tacotron_handler = TacotronHandler()
tacotron_handler.initialize()

# Create your views here.
@api_view(['GET'])
@never_cache
def test_api(request):
    return Response({'response':"You are successfully connected to Peer API"})


@api_view(['POST'])
def tts_transcription(request):
    text = request.data.get('text')
    input_sequence = tacotron_handler.preprocess(text)

    output_audio, inference_time = tacotron_handler.inference(input_sequence)
    store_path = tacotron_handler.postprocess(output_audio, filename='tts_output')

    audio = TTSSound.objects.create(
        audio_join=store_path,
        text_content=text,
        inference_time=inference_time
    )
    serializer = TTSOutputSerializer(audio)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def empty_folder(request):
    folder_input = 'Audio_Outputs/'
    for filename in os.listdir(folder_input):
        file_path = os.path.join(folder_input, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

    return Response({'response': "Media folders were cleaned up!!"})