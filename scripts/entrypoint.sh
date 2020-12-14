#!/bin/bash
set -e

VENV_DIR_PATH=/tacotron_app/virtualenv

# create virtualenv if is not set:
# create virtualenv if doesn't exist
if [ ! -d $VENV_DIR_PATH/bin ]; then
  virtualenv --system-site-packages $VENV_DIR_PATH
fi


# activate virtualenv
. $VENV_DIR_PATH/bin/activate

# install requirements in the virtualenv
if [ "$#" -eq 0 ]; then
  # install or update requirements
  pip install -r /requirements.txt
fi

uswgi --socket :8000 --master --enable-threads --module Tacotron_TTS.wsgi
