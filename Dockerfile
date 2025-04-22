FROM python:3.11.7-bookworm

ENV TZ=Asia/Seoul
WORKDIR /app

ENV PORT=80
ENV PYTHONPATH=/app

COPY requirements.txt .

RUN apt-get update && apt-get -y install cron vim
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY crontab /etc/cron.d/crontab
COPY . .

RUN chmod 0644 /etc/cron.d/crontab
RUN mkdir -p /var/log/notify
RUN mkdir -p /var/log/weather

CMD ["sh","start.sh"]