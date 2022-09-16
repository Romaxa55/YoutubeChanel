import Class.Auth
import time
import multiprocessing as mp
import settings
import ast


class Youtube(Class.Auth.Auth):

    def __init__(self):
        self.lang = None
        self.Lang_file = None
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

    def createPlaylists(self, args):
        request = self.youtube().playlists().insert(
            part="snippet,status",
            body=args
        )
        print(args)
        request.execute()
        return request

    @staticmethod
    def MultiProcessStart(method, args):
        num = len(args)
        if num != 0:
            for i in args:
                p = mp.Process(target=method, args=(i,))
                p.start()
                # Ограничу в 5 потоков в секунду
                if num % 2 == 0:
                    p.join()
                    time.sleep(1)
                num += 1
            time.sleep(2)
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

    def CreateWhiteList(self, args):
        self.Lang_file = settings.lang_file
        print(self.Lang_file)
        with open(self.Lang_file) as f:
            self.lang = ast.literal_eval(f.read())
        for k, v in self.lang.items():
            args.append(f"My Works. {k.title()} language ({v})")
        return args


    def __del__(self):
        print(f"{self.__class__} FINISHED")
        print(time.time() - self.start_time)
