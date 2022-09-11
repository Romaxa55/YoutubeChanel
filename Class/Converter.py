import ast
import json
import multiprocessing
import time
import moviepy.editor as mp
from moviepy.video.VideoClip import TextClip
import settings


class Converter:
    lang = None
    filename = None

    def __init__(self):
        self.start_time = time.time()
        self.Lang_file = settings.lang_file
        with open(self.Lang_file) as f:
            self.lang = ast.literal_eval(f.read())

    def createVideo(self):
        names = []
        s = settings
        print(s.config['TitleCanvas'])
        for k, v in self.lang.items():
            names.append(f"{s.MEDIA_DIR}"
                         f"{s.config['Project']}/"
                         f"{s.config['Project']}_{v}.mov")
        p = multiprocessing.Pool()
        p.map(self.RenderVideo, names)

    def AddSub(self, input):
        input = input.rsplit(".", 1)[0]

        file = f"{input}.txt"
        with open(file, 'r') as fp:
            data = json.load(fp)
        print(data)

    def RenderVideo(self, input):
        self.AddSub(input)
        # clip = mp.VideoFileClip(input).subclip(0, 20)
        # clip.write_videofile(input)
        return input

    def __del__(self):
        print(time.time() - self.start_time)

