import os
import sys
from collections import defaultdict

import yaml
from os.path import exists as file_exists

# GLOBAL DIRS
#######################
BASEDIR = os.getcwd() + "/"
MEDIA_DIR = os.getcwd() + "/Video/"
########################

# SETTINGS
#######################

# File list langs translates
lang_file: str = "config/locale.list"

# Config file config
Config_file: str = "Video/Terminator/config.yaml"
# Original video file name in folder ./Video/

# Files with tokens for YouTube
APP_TOKEN_FILE = "YOUR_CLIENT_SECRET_FILE.json"
USER_TOKEN_FILE = "user_token.json"

# Youtube scopes
SCOPES = [
    'https://www.googleapis.com/auth/youtube.force-ssl',
    'https://www.googleapis.com/auth/userinfo.profile',
    # 'https://www.googleapis.com/auth/youtube.upload',
    # 'https://www.googleapis.com/auth/userinfo.email'
]

try:
    os.chdir(BASEDIR)
    error = False
    with open(Config_file, 'r') as file:
        config = yaml.safe_load(file)

    global_vars = {
        "lang_file": {"name": lang_file, "Path": BASEDIR},
        "Video_file": {"name": config['Video_file'], "Path": MEDIA_DIR + config['Project'] + "/"}
    }
    global_params = defaultdict(list)

    key: str
    for key, value in global_vars.items():
        path = "".join(str(v) for k, v in sorted(value.items()))
        f = open(path, 'rb')
        global_params[key].append(path)

    print("Current working directory: {0}".format(os.getcwd()))
except FileNotFoundError:
    print("File: {0} not exist".format(path))
    sys.exit()
except NotADirectoryError:
    print("{0} is not a directory".format(BASEDIR))
except PermissionError:
    print("You do not have permissions to change to {0}".format(BASEDIR))
