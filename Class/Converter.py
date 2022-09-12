import ast
from os.path import exists as file_exists
import multiprocessing
import pickle
import time
from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip

import settings


class Converter:
    lang = None
    originalVideoFile: str = None
    langNow : str = None

    def __init__(self):
        self.start_time = time.time()
        self.Lang_file = settings.lang_file
        self.originalVideoFile = settings.global_params['Video_file'][0]
        with open(self.Lang_file) as f:
            self.lang = ast.literal_eval(f.read())

    # Формируем список видео для каждой страны свое
    def createVideo(self):
        names = []
        s = settings
        for k, v in self.lang.items():
            names.append(f"{s.MEDIA_DIR}"
                         f"{s.config['Project']}/"
                         f"{s.config['Project']}_{v}.mov")

        # p = multiprocessing.Pool(multiprocessing.cpu_count())
        p = multiprocessing.Pool(3)
        # Мультипоточность вызывам RenderVideo
        p.map(self.RenderVideo, names)

    def RenderVideo(self, input):
        # Работаем с оригинальным файлом
        if not file_exists(input):
            print(f"{input} not exist")
            clip = self.AddSub(input)
            clip.write_videofile(
                input,
                fps=clip.fps,
                remove_temp=True,
                codec="libx264",
                audio_codec="aac"
            )
        else:
            clipOriginal = VideoFileClip(self.originalVideoFile).duration
            clipSource = VideoFileClip(input).duration
            if int(clipOriginal) == int(clipSource):
                print("+ [GOOD] " + input)
            else:
                os.remove(input)
                self.RenderVideo(input)

    # Method return font file for subtitles
    def switch(self, lang):
        fontPath = settings.BASEDIR + "fonts"
        if file_exists(fontPath + "/" + lang + ".ttf"):
            return fontPath + "/" + lang + ".ttf"
        else:
            return "Times-New-Roman"

    def AddSub(self, input):
        input = input.rsplit(".", 1)[0]
        langNow = input
        langNow = langNow.split("_", 1)[1]

        # Read original video
        clip = VideoFileClip(self.originalVideoFile)

        # Add logo
        logoPath = f"{settings.BASEDIR}Gifs/logo.png"
        logo = (ImageClip(logoPath)
                .set_duration(clip.duration)
                .resize(height=70)  # if you need to resize...
                .margin(left=20, top=20, opacity=0)  # (optional) logo-border padding
                .set_pos(("left", "top")))

        # Add Subscribe watermark
        watermarkPath = f"{settings.BASEDIR}Gifs/Yotube hello.mov"
        watermark = (VideoFileClip(watermarkPath, has_mask=True)
                     .set_duration(12.47)
                     .resize(height=600)
                     .margin(right=8, top=8, opacity=0)
                     .set_pos(('right', 'bottom')))

        # Add Subs
        font = self.switch(langNow)
        print(f"Use font {font} for lang {langNow}")
        generator = lambda txt: TextClip(
            txt,
            font=font,
            fontsize=70,
            color='white'
        )
        file = f"{input}.bin"

        # Read subs from dump file
        with open(file, 'rb') as f:
            sub = pickle.load(f)
        subtitles = SubtitlesClip(sub, generator)

        # Return result merge original + subtitles + watermark + logo
        return CompositeVideoClip([
            clip,
            subtitles.set_position(('center', 'bottom')).margin(bottom=20, opacity=0),
            watermark.set_start(t=clip.duration - 12.47 - 15),
            watermark.set_start(t=clip.duration * 0.5),
            logo
        ])

    def __del__(self):
        print(time.time() - self.start_time)
