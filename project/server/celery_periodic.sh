#!/bin/bash

python3.9 -m celery -A app.celery beat --max-interval 1 -l info
