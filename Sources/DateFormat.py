#!/usr/bin/env python

import os
import datetime




class DateFormat(object):
    def getData(self):
        now = datetime.datetime.now()
        dateStr = now.strftime('%Y-%m-%d %H:%M:%S')
        print(dateStr)
        archivePath = '//Users/shanwz/Desktop/' + '/BuildFile/' + dateStr + '/'
        isExists = os.path.exists(archivePath)
        if isExists:
            pass
        else:
            os.makedirs(archivePath)
