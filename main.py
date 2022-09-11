# -*- coding: utf-8 -*-

# Sample Python code for youtube.channels.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python
import glob
import json
import settings

from moviepy.editor import *
from collections import defaultdict
import googleapiclient
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from deep_translator import GoogleTranslator, LingueeTranslator, PonsTranslator, MyMemoryTranslator, YandexTranslator
import ast
from moviepy.video.tools.subtitles import SubtitlesClip
import time
import queue  # imported for using queue.Empty exception
from multiprocessing import Lock, Process, Queue, current_process
from Class.Translate import *
from Class.Converter import *

SCOPES = [
    'https://www.googleapis.com/auth/youtube.force-ssl',
    'https://www.googleapis.com/auth/userinfo.profile',
    # 'https://www.googleapis.com/auth/youtube.upload',
    # 'https://www.googleapis.com/auth/userinfo.email'
]
APP_TOKEN_FILE = "YOUR_CLIENT_SECRET_FILE.json"
USER_TOKEN_FILE = "user_token.json"


def pretty(d, indent=0):
    for key, value in d.items():
        print('\t' * indent + str(key))
        if isinstance(value, dict):
            pretty(value, indent + 1)
        else:
            print('\t' * (indent + 1) + str(value))


def get_creds_cons():
    flow = InstalledAppFlow.from_client_secrets_file(APP_TOKEN_FILE, SCOPES)
    return flow.run_console()


def get_creds_saved():
    # https://developers.google.com/docs/api/quickstart/python
    creds = None

    if os.path.exists(USER_TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(USER_TOKEN_FILE, SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(APP_TOKEN_FILE, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(USER_TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

    return creds


def youtube():
    # creds = get_creds_cons()
    credentials = get_creds_saved()
    service = googleapiclient.discovery.build(
        "youtube", "v3", credentials=credentials)
    return service


def get_video_info(id, part='snippet'):
    request = youtube().videos().list(
        part=part,
        id=id
    )
    response = request.execute()

    response = {
        'title': json.dumps(response['items'][0]['snippet']['title'], ensure_ascii=False).strip('"«» „“'),
        'description': json.dumps(response['items'][0]['snippet']['description'], ensure_ascii=False).replace("\\n",
                                                                                                              "\n").strip(
            '"«» „“')
    }
    return response


def update_video_info(videoID='', trans='', tags=[]):
    td = get_video_info(videoID)
    snippet = {"defaultLanguage": "ru",
               "localized": td,
               'defaultAudioLanguage': 'ru',
               "categoryId": "22",
               "tags": tags,
               "title": f"{td['title']}",
               "description": f"{td['description']}"
               }
    request = youtube().videos().update(
        part="localizations,snippet",
        body={
            "id": videoID,
            "localizations": trans,
            "snippet": snippet
        }
    )
    response = request.execute()

    print(response)


def translate(d):
    with open('locale.list') as f:
        data = f.read()
    lang = ast.literal_eval(data)
    result = {}
    for k, v in lang.items():
        title = GoogleTranslator(source='auto', target=v).translate(d['title']).strip('"«» „“')
        description = GoogleTranslator(source='auto', target=v).translate(d['description']).strip('"«» „“')
        result[v] = {"title": title, "description": description}
        print(f"Язык {k}")
        print({"title": title, "description": description})
    return result


def converter(clip, filename, sub, lang):
    # clip = clip.subclip(0, 30)
    print(f"clip = {clip}")
    print(f"filename = {filename}")
    print(f"sub = {sub}")
    print(f"lang = {lang}")
    # Text for Subtitles
    gen = lambda txt: TextClip(txt, font='Arial', fontsize=70, color='white')
    # Init Subtitles
    subtitles = SubtitlesClip(sub, gen)
    # Create Subtitles
    clip = CompositeVideoClip([clip, subtitles.set_pos(('center', 'bottom'))])
    # init video Subcribe duration
    water_duration = 12.47
    # Create Subcribe
    watermark = (VideoFileClip("./Gifs/Yotube hello.mov", has_mask=True)
                 .set_duration(water_duration)
                 .resize(height=600)
                 .margin(right=8, top=8, opacity=0.3)
                 .set_pos(('right', 'bottom')))
    # Create Subcribe to end video 15 sec + 12.47 = 27 sec
    clip = CompositeVideoClip([clip, watermark.set_start(t=clip.duration - water_duration + 15)])  # set_start(t=5)
    # Create Subcribe to begin video from 30% video
    # clip = CompositeVideoClip([clip, watermark.set_start(t=clip.duration*0.3)]) #set_start(t=5)
    # Add Logo
    logo = (ImageClip("./Gifs/logo.png")
            .set_duration(clip.duration)
            .resize(height=150)  # if you need to resize...
            .margin(left=20, top=20, opacity=0)  # (optional) logo-border padding
            .set_pos(("left", "top")))
    # Create Logo
    # clip = CompositeVideoClip([clip, logo]) #set_start(t=5)
    # Build
    clip.write_videofile(f"./Video/{lang}_{filename}", fps=clip.fps,
                         codec="libx264", threads=12)


def main():
    # File list langs translates
    Lang_file = settings.global_params['lang_file'][0]

    # Original video file name in folder ./Video/
    Video_file = settings.global_params['Video_file'][0]

    Tags = settings.config['tags']

    #######################
    # id Video on youtube
    id = 'FWnJKjmgXf8'
    # tags for video


    # ToDo Добавить автора и название картины в переменную
    canvas = {"title": "Терминатор", "who": "Арнольд Шварценеггер"}
    # Update video manifest< add translate, tags, etc...
    # update_video_info(id, translate(get_video_info(id)),tags)

    ########################################################################
    # Create Video with sub, logo, watermark
    # # Init here, need clip.duration object
    clip = VideoFileClip(Video_file)
    subs = [
        (((clip.duration * 0.1), (clip.duration * 0.1) + 2), 'Привет'),
        ((((clip.duration * 0.1) + 3), (clip.duration * 0.1) + 4), 'Приятного просмотра!!!'),
        ((((clip.duration * 0.1) + 3), (clip.duration * 0.1) + 4), 'пишем картину'),
        ((((clip.duration * 0.1) + 5), (clip.duration * 0.1) + 7), settings.config['WhoOnCanvas']),
        ((((clip.duration * 0.1) + 7), (clip.duration * 0.1) + 9), settings.config['TitleCanvas']),
        ((((clip.duration * 0.1) + 9), (clip.duration * 0.1) + 13), '‿︵‿ヽ(°□° )ノ︵‿︵'),
        (((clip.duration * 0.8), (clip.duration * 0.8) + 2), 'пожалуйста '),
        ((((clip.duration * 0.8) + 2), (clip.duration * 0.8) + 4), 'подпишись на канал'),
        ((clip.duration * 0.97 - 2, clip.duration * 0.97), 'Спасибо за просмотр!!!'),
        ((clip.duration * 0.97, clip.duration), '(o˘◡˘o)-> на забудь подписаться')
    ]
    # Create Subs
    t = Translate(Lang_file, Video_file)
    t.translateSub(subs)
    # # Create Video
    # c = Converter()
    # c.createVideo()

    # Create sub and translate other language
    # sub = createSub(subs)
    # Get num CPU
    # POOL_SIZE = os.cpu_count()

    # Create video with logo, watermark, subtitles use multithreading
    # with Executor(max_workers=POOL_SIZE) as executor:
    #     futures = []
    #     for lang in sub:
    #         futures.append(
    #             executor.submit(
    #                 converter, clip=clip, filename=filename, sub=sub[lang], lang=lang
    #             )
    #         )


if __name__ == "__main__":
    main()
