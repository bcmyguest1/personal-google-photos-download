Python code to download all photos in a user's Google Photos library

Command line arguments:
[required] credentials_file_path: assumed to be in the working directory of the script if the path is not specified. More info here: https://developers.google.com/workspace/guides/create
[optional] token_file_path: assumed to be in the working directory of the script if the path is not specified. This is a refresh token file provided by Google



Prerequisites: Must have installed python, and installed the packages in requirements.txt. Recommended to use a virtual environment so that there are no conflicts with other python code you may be running
Install Command: pip install -r requirements.txt

Run Command: python.exe download_google_photos --credentials_file_path <credentials_file_path> --token_file_path <token_file_path>