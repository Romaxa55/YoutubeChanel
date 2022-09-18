import Class.Auth
import Class.Translate
import time
import multiprocessing as mp
import settings
import ast
import os.path
import yaml


class Youtube(Class.Auth.Auth, Class.Translate.Translate):

    def __init__(self):
        self.lang = None
        self.Lang_file = None
        self.start_time = time.time()
        print(f"{self.__class__} STARTED")

    def GetVideoInfo(self, id, part='snippet, status'):
        request = self.youtube().videos().list(
            part=part,
            id=id
        )
        response = request.execute()
        return response

    def GetPlaylists(self):

        request = self.youtube().playlists().list(
            part="snippet",
            maxResults=50,
            mine=True
        )
        response = request.execute()
        return response

    def CreatePlaylists(self, args):
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
                # Ограничу в 2 потоков в секунду
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
    def DeletePlaylist(self, whitelist):
        blacklist = []
        for i in self.getPlaylists()['items']:
            if not (i['snippet']['title'] in whitelist):
                blacklist.append(i['id'])
        # Use Multiprocessing
        status = self.MultiProcessStart(self.DeletePlaylistMP, blacklist)
        return status

    # Doing method delete Plst
    def DeletePlaylistMP(self, id_pls: str) -> str:
        request = self.youtube().playlists().delete(
            id=id_pls
        )
        response = request.execute()
        return response

    def UpdateVideoInfo(self, videoID={}):
        print(videoID)
        for id in videoID:
            for LANG, ID in id.items():
                title = self.translate(settings.config['Title'], LANG)
                description = self.translate(settings.config['Description'], LANG)
                # newTags = []
                print(f"Create New video from original text on {LANG}")
                # for tag in settings.config['tags']:
                #     newTags.append(self.translate(tag, LANG))
                # print(newTags)
                snippet = {"defaultLanguage": LANG,
                           'defaultAudioLanguage': LANG,
                           "categoryId": "22",
                           "tags": settings.config['tags'],
                           "title": title,
                           "description": description
                           }
                status = {'privacyStatus': 'public',
                          'license': 'youtube',
                          'embeddable': True,
                          'publicStatsViewable': True,
                          'madeForKids': False,
                          'selfDeclaredMadeForKids': False}
                # youtube = self.youtube()
                request = self.youtube().videos().update(
                        part="snippet, status",
                        body={
                            "id": ID,
                            "snippet": snippet,
                            "status": status
                        }
                    )
                response = request.execute()
                print(response)

                project = settings.config['Project']
                image = f"{settings.BASEDIR}Video/{project}/" \
                        f"{project}_{LANG}.png"
                # print(self.SetThumbnails(ID, image))

    def CreateWhiteList(self):
        self.Lang_file = settings.lang_file
        print(self.Lang_file)
        with open(self.Lang_file) as f:
            self.lang = ast.literal_eval(f.read())
        for k, v in self.lang.items():
            args.append(f"My Works. {k.title()} language ({v})")
        return args

    def ResumableUpload(self, request, retries=5):
        while retries > 0:
            try:
                status, response = request.next_chunk()
                if response is None: continue
                if 'id' not in response: raise Exception("no id found while video uploading")

                return response  # success
            except Exception as e:
                print(e)
                retries -= 1
                sleep(randrange(5))

        return None

    def ListTranslatedTitle(self):
        self.Lang_file = settings.lang_file
        with open(self.Lang_file) as f:
            self.lang = ast.literal_eval(f.read())
        for k, v in self.lang.items():
            title = self.translate(settings.config['Title'], v)
            description = self.translate(settings.config['Description'], v)
            print(f"Lang {k}:{v}")
            print(f"{title}")
            print(f"{description}")

    def YoutubeVideoUpload(self):
        self.Lang_file = settings.lang_file
        with open(self.Lang_file) as f:
            self.lang = ast.literal_eval(f.read())
        project = settings.config['Project']
        # tested
        # self.lang = {'georgian': 'ka'}
        for k, v in self.lang.items():
            skip = False
            file = f"{settings.BASEDIR}Video/{project}/" \
                   f"{project}_{v}.mov"
            image = f"{settings.BASEDIR}Video/{project}/" \
                    f"{project}_{v}.png"
            file_exists = os.path.exists(file)
            if file_exists:
                # Status Upload file create
                status_file = f"{settings.BASEDIR}Video/{project}/" \
                              f"status.yaml"
                if not os.path.exists(status_file):
                    with open(status_file, 'w'): pass

                with open(status_file, 'r') as f:
                    status = yaml.safe_load(f)

                # Checked exist file
                if status is not None:
                    if file in status:
                        print(f"File is {file} exist in {status} ")
                        print("SKIP STAGE")
                        skip = True
                else:
                    status = []

                # Init media file upload
                title = self.translate(settings.config['Title'], v)
                description = self.translate(settings.config['Description'], v)

                meta = {
                    'snippet': dict(
                        # defaultLanguage=v,
                        # defaultAudioLanguage=v,
                        categoryId="22",
                        tags=title.split(","),
                        title=title,
                        description=description),
                    "status": dict(
                        privacyStatus="private",
                        license="youtube",
                        embeddable=True,
                        publicStatsViewable=True,
                        madeForKids=False,
                        selfDeclaredMadeForKids=False
                    )
                }
                youtube = self.youtube()
                insert_request = youtube.videos().insert(
                    part=','.join(meta.keys()),
                    body=meta,
                    media_body=self.upload(file)
                )
                if not skip:
                    r = self.ResumableUpload(insert_request)
                    print(r)
                    if 'id' in r:
                        status.append(file)
                        with open(status_file, 'w') as outfile:
                            yaml.dump(status, outfile, default_flow_style=False, allow_unicode=True)
                            return True

    def SetThumbnails(self, idVideo, image):
        youtube = self.youtube()
        insert_request = youtube.thumbnails().set(
            videoId=idVideo,
            media_body=self.uploadThumbnails(image)
        )
        r = insert_request.execute()
        return r

    def __del__(self):
        print(f"{self.__class__} FINISHED")
        print(time.time() - self.start_time)
