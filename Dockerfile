FROM python:3.11.7-bookworm

ENV TZ=Asia/Seoul
WORKDIR /app

ENV PORT=8000
ENV PYTHONPATH=/app

COPY crontab /etc/cron.d/crontab
COPY . .

RUN apt-get update && \
    apt-get install -y --no-install-recommends cron vim && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

RUN chmod 0644 /etc/cron.d/crontab
RUN chmod +x start.sh
RUN mkdir -p /var/log/news /var/log/youtube

CMD ["sh","start.sh"]