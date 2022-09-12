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



    def __del__(self):
        print(self.__class__.__name__ + ": " + time.time() - self.start_time)
