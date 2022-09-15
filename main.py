# -*- coding: utf-8 -*-

# Sample Python code forR youtube.channels.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python
import pprint
import json
import settings

from Class.Translate import *
from Class.Converter import *
from Class.Youtube import *


#
#
# def get_video_info(id, part='snippet'):
#     request = youtube().videos().list(
#         part=part,
#         id=id
#     )
#     response = request.execute()
#
#     response = {
#         'title': json.dumps(response['items'][0]['snippet']['title'], ensure_ascii=False).strip('"«» „“'),
#         'description': json.dumps(response['items'][0]['snippet']['description'], ensure_ascii=False).replace("\\n",
#                                                                                                               "\n").strip(
#             '"«» „“')
#     }
#     return response

#
# def update_video_info(videoID='', trans='', tags=[]):
#     td = get_video_info(videoID)
#     snippet = {"defaultLanguage": "ru",
#                "localized": td,
#                'defaultAudioLanguage': 'ru',
#                "categoryId": "22",
#                "tags": tags,
#                "title": f"{td['title']}",
#                "description": f"{td['description']}"
#                }
#     request = youtube().videos().update(
#         part="localizations,snippet",
#         body={
#             "id": videoID,
#             "localizations": trans,
#             "snippet": snippet
#         }
#     )
#     response = request.execute()
#
#     print(response)


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


# Original sub
def sub():
    Video_file = settings.global_params['Video_file'][0]
    clip = VideoFileClip(Video_file)
    start_time = 5
    return [
        ((start_time, start_time + 2), 'Привет'),
        ((start_time + 2, start_time + 4), 'Приятного просмотра!!!'),
        ((start_time + 4, start_time + 6), 'пишем картину'),
        ((start_time + 6, start_time + 9), settings.config['WhoOnCanvas']),
        ((start_time + 9, start_time + 11), settings.config['TitleCanvas']),
        ((start_time + 11, start_time + 12), '‿︵‿ヽ(°□° )ノ︵‿︵'),
        (((clip.duration * 0.8), (clip.duration * 0.8) + 2), 'пожалуйста '),
        ((((clip.duration * 0.8) + 2), (clip.duration * 0.8) + 4), 'подпишись на канал'),
        ((clip.duration * 0.97 - 3, clip.duration * 0.97), '(o˘◡˘o)-> Спасибо за просмотр!!!')
    ]


def main():
    # Id Video
    id = 'FWnJKjmgXf8'

    # File list langs translates
    Lang_file = settings.global_params['lang_file'][0]

    # Original video file name in folder ./Video/
    Video_file = settings.global_params['Video_file'][0]

    Tags = settings.config['tags']

    #######################
    # Create Video with sub, logo, watermark

    # Create original syb type tuple
    subs = sub()

    # # Stage Create Subs
    # t = Translate(Lang_file, Video_file)
    # t.translateSub(subs)
    #
    # # Stage Create Video
    # c = Converter()
    # c.createVideo()

    # Stage Auth YouTube
    y = Youtube()
    whitelist = ['Art Works']
    while y.deletePlaylist(whitelist):
        pass

    # y.createPlaylists(range(1, 70))



if __name__ == "__main__":
    main()
