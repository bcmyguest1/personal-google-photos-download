from __future__ import print_function
import os.path
import traceback

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
from google_photos_api import GooglePhotosApi
from photo_downloader import PhotoDownloader
import argparse

SCOPES = ['https://www.googleapis.com/auth/photoslibrary.readonly']


def main():
    try:
        parser = argparse.ArgumentParser(description='Allow for credentials files to be passed as command line args')

        parser.add_argument('--credentials_file_path', dest='credentials_file_path', required=True,
                            help="credentials file, see https://developers.google.com/workspace/guides/create"
                                 "-credentials. "
                                 "You may provide the full path or just the file name if it is at the same level as "
                                 "the "
                                 "code")
        parser.add_argument('--token_file_path', dest='token_file_path', required=False, default='token.json',
                            help='token file, generated on login using credentials file')
        args = parser.parse_args()
        credentials_path: str = args.credentials_file_path
        token_path: str = args.token_file_path
        working_directory: str = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

        if not os.path.isfile(credentials_path):
            credentials_path = working_directory + os.sep + credentials_path

        if not os.path.isfile(token_path):
            token_path = working_directory + os.sep + token_path

        credentials: Credentials = get_google_api_creds(credentials_path, token_path)
        photos_api = GooglePhotosApi(creds=credentials)
        photo_downloader: PhotoDownloader = PhotoDownloader(photos_api=photos_api)
        photo_downloader.download_all_photos()
        print("Download of files completed")
    except Exception as e:
        print(f"Exception occurred during processing: {str(e)}")
        traceback.print_exc()


def get_google_api_creds(cred_file: str, token_file: str) -> Credentials:
    print("obtaining credentials")
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                cred_file, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_file, 'w') as token:
            token.write(creds.to_json())
    return creds


if __name__ == '__main__':
    main()
