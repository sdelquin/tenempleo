#!/bin/bash

source ~/.pyenv/versions/tenempleo/bin/activate
cd "$(dirname "$0")"
exec python main.py $@
