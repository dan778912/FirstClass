#!/bin/bash
export FLASK_ENV=development
export PROJ_DIR=$PWD
export DEBUG=1
# run our server locally:
PYTHONPATH=$(pwd):$PYTHONPATH
export FLASK_APP=server.endpoints
python3 -m flask run --debug --host=127.0.0.1 --port=8000
