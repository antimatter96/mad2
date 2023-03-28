#!/bin/bash

python3.9 -m celery -A app.celery worker -l info
