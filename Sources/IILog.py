#!/usr/bin/env python


'''
    Custom print function
    Print succeed!
    Print faild!
'''


class IILog(object):

    def __init__(self):
        pass

    # green character & white bg
    def successPrint(self,infos):
        print('\033[0;32m' + infos)

    # red character & white bg
    def failPrint(self,infos):
        print('\033[0;31m' + infos)