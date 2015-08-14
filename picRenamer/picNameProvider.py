__author__ = 'wojtek'

import os
import re
import time
import datetime

for root, dirs, files in os.walk('/home/wojtek/VBoxShared/pics'):
    print("--------------------")
    print(root)

    fre = r"(\d\d.\d\d.\d\d)_(\d+)"
    key = lambda x: int(re.match(fre, x).group(2))

    files = list(filter(lambda x: re.match(fre, x) is not None, files))
    files.sort(key=key)

    if len(files) > 0:
        startM = key(min(files, key=key))
        endM = key(max(files, key=key))
        step = 61/(endM+2-startM)
        print(startM, endM, step)

    for file in files:

        regex = r"(\d\d.\d\d.\d\d)_(\d+)_(.*)"
        m = re.match(regex, file)

        sDate = m.group(1)
        index = int(m.group(2))-startM+1
        suffix = m.group(3)
        hour = int(os.path.basename(root))

        timeFormat = "%y.%m.%d"
        tDate = time.strptime(sDate, timeFormat)
        oldDate = datetime.datetime(*tDate[:6])

        newDate = oldDate + datetime.timedelta(hours=hour, minutes=step*index)

        newTimeFormat = "%y.%m.%d_%H.%M.%S"
        newFile = "{0}_{1}".format(newDate.strftime(newTimeFormat), suffix)

        oldPath = os.path.join(root, file)
        newPath = os.path.join(os.path.dirname(root), newFile)
        print("{0}\t->\t{1}".format(oldPath, newPath))

        os.rename(oldPath, newPath)
