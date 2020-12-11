FROM anibali/pytorch:1.5.0-cuda10.2

LABEL Aymane Hachcham <ai5@spotbills.com>

ENV DEBIAN_FRONTEND noninteractive

ENV PATH="/scripts:${PATH}"

COPY ../requirements.txt /requirements.txt

RUN mkdir /tacotron-infer
