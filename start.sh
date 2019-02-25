#!/bin/bash

source venv/bin/activate
FLASK_ENV=production FLASK_APP=ssi/app.py python3 -m flask run
