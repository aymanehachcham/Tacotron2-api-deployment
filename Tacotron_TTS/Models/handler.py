
import os
import torch
import time
import logging
import uuid
import numpy as np
import torch.nn as nn
from .tacotron_model import Tacotron2
from .glow import WaveGlow
from .text_utils import Hparams, symbols
from .text_utils import text_to_sequence
from scipy.io.wavfile import write


logger = logging.getLogger(__name__)

_WORK_DIR = 'Models/'
_MODEL_DIR = 'model_checkpoints'
_AUDIO_DIR = './Audio_Outputs/'

tacotron_hparams = Hparams({
    'mask_padding': True,
    'fp16_run': False,
    'n_mel_channels': 80,
    'n_frames_per_step': 1,
    'n_symbols': len(symbols),
    'symbols_embedding_dim': 512,
    'postnet_embedding_dim': 512,
    'postnet_kernel_size': 5,
    'postnet_n_convolutions': 5,
    'encoder_n_convolutions': 3,
    'encoder_embedding_dim': 512,
    'encoder_kernel_size': 5,
    'attention_rnn_dim': 1024,
    'attention_dim': 128,
    'decoder_rnn_dim': 1024,
    'prenet_dim': 256,
    'max_decoder_steps': 1000,
    'gate_threshold': 0.5,
    'p_attention_dropout': 0.1,
    'p_decoder_dropout': 0.1,
    'attention_location_n_filters': 32,
    'attention_location_kernel_size': 31,
    'sampling_rate': 22050
})

waveglow_params = Hparams({
    'n_mel_channels': 80,
    'n_flows': 12,
    'n_group': 8,
    'n_early_every': 4,
    'n_early_size': 2,
})

WN_config = Hparams({
    'n_layers': 8,
    'n_channels': 256,
    'kernel_size': 3
})

class TacotronHandler(nn.Module):
    def __init__(self):
        super().__init__()
        self.tacotron_model = None
        self.waveglow = None
        self.device = None
        self.initialized = None


    def _load_tacotron2(self, checkpoint_file, hparams_config: Hparams):
        tacotron2_checkpoint = torch.load(os.path.join(_WORK_DIR, _MODEL_DIR, checkpoint_file))
        self.tacotron_model = Tacotron2(hparams= hparams_config)
        self.tacotron_model.load_state_dict(tacotron2_checkpoint['state_dict'])
        self.tacotron_model.to(self.device)
        self.tacotron_model.eval()

    def _load_waveglow(self, is_fp16: bool):
        waveglow_checkpoint = torch.load(os.path.join(_WORK_DIR, _MODEL_DIR, 'waveglow.pt'))
        waveglow_model = WaveGlow(
            n_mel_channels=waveglow_params.n_mel_channels,
            n_flows=waveglow_params.n_flows,
            n_group=waveglow_params.n_group,
            n_early_every=waveglow_params.n_early_every,
            n_early_size=waveglow_params.n_early_size,
            WN_config=WN_config
        )
        self.waveglow.load_state_dict(waveglow_checkpoint['state_dict'])
        self.waveglow = waveglow_model.remove_weightnorm(waveglow_model)
        self.waveglow.to(self.device)
        self.waveglow.eval()
        if is_fp16:
            from apex import amp
            self.waveglow, _ = amp.initialize(waveglow_model, [], opt_level="3")


    def initialize(self):
        if not torch.cuda.is_available():
            raise RuntimeError("This model is not supported on CPU machines.")
        self.device = torch.device('cuda')

        self._load_tacotron2(
            checkpoint_file='tacotron2.pt',
            hparams_config=tacotron_hparams)

        self._load_waveglow(is_fp16=False)
        self.initialized = True

        logger.debug('Tacotron and Waveglow models successfully loaded!')

    def preprocess(self, text_seq):
        sequence = np.array(text_to_sequence(text_seq, ['english_cleaners']))[None, :]
        sequence = torch.from_numpy(sequence).to(device=self.device, dtype=torch.int64)
        return sequence

    def inference(self, data):
        start_inference_time = time.time()
        _, mel_output_postnet, _, _ = self.tacotron_model.inference(data)
        with torch.no_grad():
            audio = self.waveglow.infer(mel_output_postnet, sigma=0.666)
        return audio, time.time() - start_inference_time

    def postprocess(self, inference_output, filename):
        audio_numpy = inference_output[0].data.cpu().numpy()
        path = os.path.join(_AUDIO_DIR, '{}{}.wav'.format(filename, uuid.uuid4().hex))
        write(path, 22050, audio_numpy)
        return path

