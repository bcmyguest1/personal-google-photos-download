import os.path
from concurrent.futures._base import wait
from concurrent.futures.thread import ThreadPoolExecutor
from datetime import datetime
from typing import Dict, List

import requests
from dateutil import parser

from google_photos_api import GooglePhotosApi


class PhotoDownloader:
    def __init__(self, photos_api: GooglePhotosApi):
        self.photos_api = photos_api

    @staticmethod
    def set_file_last_modified(file_path, dt):
        dt_epoch = dt.timestamp()
        os.utime(file_path, (dt_epoch, dt_epoch))

    @staticmethod
    def download_photo(download_directory: str, media_item: Dict[str, str]) -> None:
        url: str = media_item['baseUrl']
        if media_item['mimeType'].__contains__("image"):
            url += '=d'
        else:
            url += '=dv'
        request = requests.get(url, allow_redirects=True)
        file_name: str = media_item['filename']
        file_path: str = download_directory + file_name
        creation_time_resp: str = media_item['mediaMetadata']['creationTime']

        print(f"Getting file: {file_name}")
        open(file_path, 'wb').write(request.content)
        try:
            creation_time: datetime = parser.parse(creation_time_resp)
            PhotoDownloader.set_file_last_modified(file_path, creation_time)
        except Exception as e:
            print(f"could not modify file {file_path} - {creation_time_resp}")
        print(f"Downloaded file to: {file_path}")

    def download_all_photos(self):
        next_page_token: str = None
        results = self.photos_api.service.mediaItems().list(pageToken=next_page_token).execute()

        media_items: List[Dict[str, str]] = results.get('mediaItems', [])
        next_page_token = results.get('nextPageToken', None)

        if not media_items:
            print('No media_items found.')
        else:
            print("Getting media items")
            working_directory: str = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
            file_dir: str = working_directory + os.sep + "downloaded_media" + os.sep
            if not os.path.exists(file_dir):
                print(f"Making directory for download: {file_dir}")
                os.mkdir(file_dir)
            page: int = 1
            num_items: int = 0
            while media_items is not None and len(media_items) > 0:
                print(f"Getting page: {page} - nextPageToken: {next_page_token}")
                num_items += len(media_items)
                print(f"Total: {num_items} Items - fetching {len(media_items)}")
                with ThreadPoolExecutor(max_workers=50) as executor:
                    res = [executor.submit(PhotoDownloader.download_photo, file_dir, media_item) for media_item in media_items]
                    wait(res)

                results = self.photos_api.service.mediaItems().list(pageToken=next_page_token).execute()
                media_items: List[Dict[str, str]] = results.get('mediaItems', [])
                next_page_token = results.get('nextPageToken', None)
                page += 1
