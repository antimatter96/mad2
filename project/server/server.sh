#!/bin/bash

python3.9 -m flask db upgrade
python3.9 -m gunicorn app:app --worker-class gevent --bind 127.0.0.1:8080
