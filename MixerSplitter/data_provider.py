__author__ = 'wojtek'

import sys
sys.path.insert(0, '/home/wojtek/CodeSpace/Python/python_start/common/')
sys.path.insert(0, '/home/wojtek/CodeSpace/Python/libs/')

import os
import re
import time
from prt import *
from pydub import AudioSegment

def crawl_files(root_path):
    for root, dirs, files in os.walk(root_path):
        print("--------------------")
        print(root)

        fre = r"(.*)\.mp3"
        key = lambda x: re.match(fre, x).group(1)

        files = list(filter(lambda x: re.match(fre, x) is not None, files))
        files.sort(key=key)

        for file in files:
            name = key(file)
            text = name + ".txt"
            text_path = os.path.join(root, text)
            mp3_path = os.path.join(root, file)

            if os.path.exists(text_path):
                yield (text_path, mp3_path, name, root)
            else:
                print(std_list(name, "Fail"))

        break

def load_cut_instructions(text_path):
    with open(text_path, "r") as f:
        for line in f:
            fre = r"(\d\d:\d\d:\d\d) (.*)"
            gs = re.match(fre, line)

            t = time.strptime(gs.group(1), "%H:%M:%S")
            name = gs.group(2)

            yield (t, name)

def load_music(mp3_path):
    return AudioSegment.from_mp3(mp3_path)

def load_data(mixes_path):
    paths = crawl_files(mixes_path)
    for path in paths:
        instructions = list(load_cut_instructions(path[0]))
        song = load_music(path[1])
        yield (instructions, song, path[2], path[3])
#
# paths = list(crawl_files('/home/wojtek/VBoxShared/Mixes'))
#
# song = load_music(paths[0][1])
#
# first_10_seconds = song[:10*60*1000]
# save = os.path.join(paths[0][3], "mashup.mp3")
# first_10_seconds.export(save, format="mp3")
#
# for line in load_cut_instructions(paths[0][1]):
#     print(line)

# print(std_list([paths[0][1], paths[0][2]]))
