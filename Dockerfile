FROM anibali/pytorch:1.5.0-cuda10.2
USER root

MAINTAINER Aymane Hachcham <aymanehachchaming@gmail.com>

ENV DEBIAN_FRONTEND noninteractive
ENV PATH="/scripts:${PATH}"

RUN apt-get update


RUN mkdir /tacotron_app
COPY ./Tacotron_TTS /tacotron_app
WORKDIR /tacotron_app


# install virtualenv
RUN pip install --upgrade pip
RUN pip install virtualenv


COPY ./requirements.txt /requirements.txt
COPY ./scripts /scripts

RUN chmod +x  /scripts/*

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static


CMD ["entrypoint.sh"]