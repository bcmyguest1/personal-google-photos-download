from typing import Tuple, List, Dict

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


class GooglePhotosApi:
    def __init__(self, creds: Credentials):
        self.service = build('photoslibrary', 'v1', credentials=creds)

    def get_paged_media_items(self, page_token: str = None) -> Tuple[List[Dict[str, str]], str]:
        print(f"Fetching media items list for page_token: {page_token}")
        results = self.service.mediaItems().list(pageToken=page_token, pageSize=100).execute()
        media_items: List[Dict[str, str]] = results.get('mediaItems', [])
        next_page_token = results.get('nextPageToken', None)
        print(results)
        return media_items, next_page_token