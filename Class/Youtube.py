import Auth

from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import googleapiclient
from googleapiclient.discovery import build

import settings
import time


class Youtube(Auth):
    def __init__(self):
        self.start_time = time.time()
        print(f"{self.__class__} STARTED")

    def __del__(self):
        print(f"{self.__class__} FINISHED")
        print(time.time() - self.start_time)
