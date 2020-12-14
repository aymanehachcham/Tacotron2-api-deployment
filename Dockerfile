FROM anibali/pytorch:1.5.0-cuda10.2
USER root

ENV DEBIAN_FRONTEND noninteractive


RUN apt-get update && apt-get -y install sudo
RUN apt-get install -y build-essential
RUN conda config --add channels conda-forge
RUN conda install uwsgi

#RUN useradd -m docker && echo "docker:docker" | chpasswd && adduser docker sudo

#RUN adduser --disabled-password --gecos '' newuser \
#    && adduser newuser sudo \
#    && echo '%sudo ALL=(ALL:ALL) ALL' >> /etc/sudoers

ENV PATH="/scripts:${PATH}"

# install virtualenv
#RUN pip install virtualenv


COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

#USER newuser
RUN mkdir /tacotron_app
#RUN chown newuser /tacotron_app
#USER newuser


COPY ./Tacotron_TTS /tacotron_app

WORKDIR /tacotron_app
COPY ./scripts /scripts

RUN chmod +x  /scripts/*

RUN mkdir -p /vol/web/media

CMD ["entrypoint.sh"]