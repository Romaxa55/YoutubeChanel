import ast
import pickle

from os.path import exists as file_exists
import time
from collections import defaultdict

from deep_translator import GoogleTranslator


class Translate:
    lang = None
    filename = None

    def __init__(self, langFile, filename):
        """

        :type filename: object
        """
        self.start_time = time.time()
        self.langFile = langFile
        self.filename = filename.rsplit(".", 1)[0]

    def __del__(self):
        print(self.__class__.__name__ + ": " + time.time() - self.start_time)

    def getList(self):  # getList method
        with open(self.langFile) as f:
            self.lang = ast.literal_eval(f.read())

    def translateSub(self, sub):
        self.getList()
        d = defaultdict(list)
        for k, v in self.lang.items():
            file = f"{self.filename}_{v}.bin"
            if not file_exists(file):
                for i in range(len(sub)):
                    d[v].append((sub[i][0],
                                 (GoogleTranslator(source='ru', target=v)
                                  .translate((sub[i][1]))),))
                # сериализовать
                print(d[v])
                with open(file, 'wb') as f:
                    print(f"[OK] {file}.")
                    pickle.dump(d[v],f)
            else:
                print(f"[OK] {file}.")
