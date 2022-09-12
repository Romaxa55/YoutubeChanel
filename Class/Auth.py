import os

from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import googleapiclient
from googleapiclient.discovery import build

import settings
import time


class Auth:
    APP_TOKEN_FILE = "YOUR_CLIENT_SECRET_FILE.json"
    USER_TOKEN_FILE = "user_token.json"

    SCOPES = [
        'https://www.googleapis.com/auth/youtube.force-ssl',
        'https://www.googleapis.com/auth/userinfo.profile',
        'https://www.googleapis.com/auth/youtube.upload',
        'https://www.googleapis.com/auth/userinfo.email'
    ]

    def __init__(self):
        self.start_time = time.time()

    def get_creds_cons(self):
        return InstalledAppFlow.from_client_secrets_file(
            self.APP_TOKEN_FILE,
            self.SCOPES
        )

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

    def auth(self):
        credentials = self.get_creds_saved()
        service = googleapiclient.discovery.build(
            "youtube", "v3", credentials=credentials)
        return service

    def __del__(self):
        print(self.__class__.__name__ + ": " + time.time() - self.start_time)
