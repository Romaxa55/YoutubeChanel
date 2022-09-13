import Class.Auth
import time


class Youtube(Class.Auth.Auth):

    def __init__(self):
        self.start_time = time.time()
        print(f"{self.__class__} STARTED")

    def getPlaylists(self):
        request = self.youtube().playlists().list(
            part="snippet,contentDetails",
            maxResults=25,
            mine=True
        )
        return request.execute()

    def __del__(self):
        print(f"{self.__class__} FINISHED")
        print(time.time() - self.start_time)
