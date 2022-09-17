import os
import time

import google_auth_oauthlib
import googleapiclient
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import settings


class Auth:
    APP_TOKEN_FILE = f"{settings.BASEDIR}{settings.APP_TOKEN_FILE}"
    USER_TOKEN_FILE = f"{settings.BASEDIR}{settings.USER_TOKEN_FILE}"
    SCOPES = settings.SCOPES

    def __init__(self):
        self.start_time = time.time()
        print(f"{self.__class__} STARTED")
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    def get_creds_cons(self):
        flow = InstalledAppFlow.from_client_secrets_file(
            self.APP_TOKEN_FILE,
            self.SCOPES
        )
        return flow.run_console()

    def get_creds_saved(self):
        creds = None
        if os.path.exists(self.USER_TOKEN_FILE):
            creds = Credentials.from_authorized_user_file(
                self.USER_TOKEN_FILE,
                self.SCOPES
            )
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.APP_TOKEN_FILE,
                    self.SCOPES
                )
                creds = flow.run_local_server(port=0)
            with open(self.USER_TOKEN_FILE, 'w') as token:
                token.write(creds.to_json())

        return creds

    def youtube(self):
        credentials = self.get_creds_saved()
        service = googleapiclient.discovery.build(
            "youtube", "v3", credentials=credentials)
        return service

    def upload(self, file):
        return MediaFileUpload(file, chunksize=-1, resumable=True)

    def uploadThumbnails(self, file):
        return MediaFileUpload(file)

    def __del__(self):
        print(f"{self.__class__} FINISHED")
        print(time.time() - self.start_time)
