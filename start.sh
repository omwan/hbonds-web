#!/bin/bash

source venv/bin/activate
source .env
FLASK_ENV=production FLASK_APP=ssi/app.py python3 -m flask run
