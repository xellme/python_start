__author__ = 'wojtek'

import sys
sys.path.insert(0, '/home/wojtek/CodeSpace/Python/python_start/common/')

import data_provider
import os
import shutil
import math
from prt import *

def create_output_dir(root, name):
    output = os.path.join(root, name)
    try:
        os.mkdir(output)
    except OSError:
        print('Already exists: {0} '.format(output))

def split_audio(instructions, song):
    def milli_time(t):
        hour_s = t.tm_hour * 60 * 60
        min_s = t.tm_min * 60
        s = t.tm_sec + hour_s + min_s
        return s * 1000

    def parse_instruction(instructions):
        inst_lst = zip(instructions, instructions[1:])
        for inst in inst_lst:
            t_start = milli_time(inst[0][0])
            t_end = milli_time(inst[1][0])
            name = inst[0][1]

            yield (t_start, t_end, name)

        inst_last = instructions[len(instructions) - 1]
        yield (milli_time(inst_last[0]), len(song), inst_last[1])

    for inst in parse_instruction(instructions):
        start = inst[0]
        end = inst [1]
        name = inst[2]
        yield (name, song[start:end])

def save_outputs(root, set_name, mix):
    print("--------------------")
    print(set_name)
    directory = os.path.join(root, set_name)

    #clear dir
    shutil.rmtree(directory, ignore_errors=True)
    #create dir
    try:
        os.mkdir(directory)
    except OSError as e:
        print("Couldn't create directory {0}, {1}".format(directory, e))

    #save ouputs in new dir
    i = 0
    for m in mix:
        i += 1

        file_name = ("{0:02d}. {1}.mp3").format(i, m[0])
        song_path = os.path.join(directory, file_name)

        song = m[1]

        #, tags={'artist': 'Various artists', 'album': 'Best of 2011', 'comments': 'This album is awesome!'})
        song.export(song_path, format="mp3", tags={'album': set_name, '#': i})
        print(file_name)

ds = data_provider.load_data('/home/wojtek/VBoxShared/Mixes')

for data in ds:
    mix = split_audio(*data[:2])
    set_name = data[2]
    root = data[3]

    save_outputs(root, set_name, mix)
