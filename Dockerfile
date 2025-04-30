FROM python:3.11.7-bookworm

ENV TZ=Asia/Seoul
WORKDIR /app

ENV PORT=80
ENV PYTHONPATH=/app

COPY crontab /etc/cron.d/crontab
COPY . .

RUN apt-get update && apt-get -y install cron vim
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

RUN chmod 0644 /etc/cron.d/crontab
RUN chmod +x start.sh
RUN mkdir -p /var/log/news /var/log/youtube

CMD ["sh","start.sh"]