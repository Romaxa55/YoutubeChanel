import Class.Auth
import time
import multiprocessing as mp


class Youtube(Class.Auth.Auth):

    def __init__(self):
        self.start_time = time.time()
        print(f"{self.__class__} STARTED")

    def get_video_info(self, id, part='snippet'):
        request = self.youtube().videos().list(
            part=part,
            id=id
        )
        response = request.execute()
        return response

    def getPlaylists(self):

        request = self.youtube().playlists().list(
            part="snippet",
            maxResults=50,
            mine=True
        )
        response = request.execute()
        return response

    def createPlaylists(self, idList):
        status = self.MultiProcessStart(
            self.createPlaylistsMP,
            idList
        )
        return status

    def createPlaylistsMP(self, args):
        snippet = {"defaultLanguage": "ru",
                   "title": str(args),
                   "description": f"321"
                   }
        request = self.youtube().playlists().insert(
            part="snippet,contentDetails",
            body={
                "snippet": snippet
            }
        )
        request.execute()
        return request

    @staticmethod
    def MultiProcessStart(method, args):
        num = len(args)
        if num != 0:
            for i in args:
                p = mp.Process(target=method,args=(i,))
                p.start()
                # Ограничу в 5 потоков в секунду
                if num % 5 == 0:
                    p.join()
                    time.sleep(1)
                num += 1
            time.sleep(1)
            p.join()
        else:
            return False
        return True
    # multiprocessing Delete method
    def deletePlaylist(self, whitelist):
        blacklist = []
        for i in self.getPlaylists()['items']:
            if not (i['snippet']['title'] in whitelist):
                blacklist.append(i['id'])
        # Use Multiprocessing
        status = self.MultiProcessStart(self.deletePlaylistMP, blacklist)
        return status

    # Doing method delete Plst
    def deletePlaylistMP(self, id_pls: str) -> str:
        request = self.youtube().playlists().delete(
            id=id_pls
        )
        response = request.execute()
        return response

    def __del__(self):
        print(f"{self.__class__} FINISHED")
        print(time.time() - self.start_time)
