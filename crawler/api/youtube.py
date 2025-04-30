from datetime import datetime, timezone
from config import GoogleConfig
from googleapiclient.discovery import build
from util import cron_log, parse_datetime_kst, is_outdated_kst

class YouTubeCrawler:
    def __init__(self):
        self.youtube = build('youtube', 'v3', developerKey=GoogleConfig.API_KEY)
        self.channel_id = None
        self.playlist_id_list = []
        self.playlist_item_list = []

    def get_channel_id(self):
        request = self.youtube.search().list(
            part='snippet',
            q="telepix110",
            type='channel',
            maxResults=1
        )
        response = request.execute()
        self.channel_id = response['items'][0]['snippet']['channelId']
        return self.channel_id

    def get_playlist_id_list(self):
        next_page_token = None

        while True:
            request = self.youtube.playlists().list(
                part='snippet',
                channelId=self.channel_id,
                maxResults=50,
                pageToken=next_page_token
            )
            response = request.execute()

            for item in response['items']:
                self.playlist_id_list.append(item['id'])

            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break

    def get_playlist_items(self, playlist_id):
        next_page_token = None
        while True:
            request = self.youtube.playlistItems().list(
                part='snippet',
                playlistId=playlist_id,
                maxResults=50,
                pageToken=next_page_token
            )
            response = request.execute()

            for item in response['items']:
                snippet = item['snippet']
                video_id = snippet['resourceId']['videoId']
                author = snippet['videoOwnerChannelTitle']
                title = snippet['title']
                url = f"https://www.youtube.com/watch?v={video_id}"
                embed_url = f"https://www.youtube.com/embed/{video_id}"  # iframe src용
                thumbnail_url = snippet['thumbnails'].get('high', {}).get('url', '')
                published_at = snippet['publishedAt']

                dt = datetime.strptime(published_at, '%Y-%m-%dT%H:%M:%SZ')
                dt = dt.replace(tzinfo=timezone.utc)

                if is_outdated_kst(parse_datetime_kst(dt), 24):
                    continue
                else:
                    cron_log(f'Youtube Scrap Success: {title}')

                self.playlist_item_list.append({
                    'author': author,
                    'title': title,
                    'url': url,
                    'embed_url': embed_url,
                    'thumbnail_url': thumbnail_url,
                    'published_at': published_at
                })

            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break

    def fetch(self):
        self.get_channel_id()

        self.get_playlist_id_list()

        for playlist_id in self.playlist_id_list:
            self.get_playlist_items(playlist_id)

        return self.playlist_item_list


