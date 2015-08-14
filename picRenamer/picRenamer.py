__author__ = 'wojtek'

import os
import re
import time
import datetime

for root, dirs, files in os.walk('/home/wojtek/VBoxShared/pics'):
    print("--------------------")
    print(root)

    for file in files:
        regex = r"(\d\d.\d\d.\d\d_\d\d.\d\d.\d\d)_(.*)"
        m = re.match(regex, file)
        if m is not None:
            sDate = m.group(1)
            suffix = m.group(2)

            timeFormat = "%y.%m.%d_%H.%M.%S"
            tDate = time.strptime(sDate, timeFormat)
            oldDate = datetime.datetime(*tDate[:6])

            newDate = oldDate + datetime.timedelta(days=1)

            newFile = "{0}_{1}".format(newDate.strftime(timeFormat), suffix)

            print("{0}\t->\t{1}".format(file, newFile))

            oldPath = os.path.join(root, file)
            newPath = os.path.join(root, newFile)

            # os.rename(oldPath, newPath)

        else:
            print("{0}\t->\tFail".format(file))
