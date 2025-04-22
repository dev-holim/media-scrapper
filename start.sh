crontab /etc/cron.d/crontab &&
uvicorn main:app --host 0.0.0.0 --port ${PORT} &&
service cron start
