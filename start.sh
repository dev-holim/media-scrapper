#!/bin/bash

crontab /etc/cron.d/crontab
cron &
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 1