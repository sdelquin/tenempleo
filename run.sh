#!/bin/bash

source ~/.virtualenvs/tenempleo/bin/activate
cd "$(dirname "$0")"
exec python main.py $@
