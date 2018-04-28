# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name       ：  PullGitFiles
   Description     ：
   Author          ：  Noah_Shan
   date            ：  2018/4/27
-------------------------------------------------
   Change Activity :   2018/4/27:
-------------------------------------------------
"""
__author__ = 'Noah_Shan'


from IILog import *
import subprocess

'''
    First : CD current file
    Second: execute 'git pull' order
'''

IILog().successPrint('### Git pull start...\n')
projectPath = ''

# get project path
def autoBuild():

    fileHandle = open('sourcePathsourceipaName.txt', 'r')
    for lineInfo in fileHandle.readlines():
        if lineInfo.__contains__('#'):
            # nothing
            continue
        elif lineInfo.__contains__('SourcePath'):
            # path
            projectPaths = lineInfo[13:].strip('\n')
            break
        else:
            # nothing
            continue
    fileHandle.close()
    return projectPaths

projectPath = autoBuild()
projectPath = '/Users/shanwz/Desktop/DingTalkCalendarVw/'


def uploadIPAFile():
    try:
        upload = subprocess.Popen('git pull', stdout=subprocess.PIPE,shell=True, cwd=projectPath)
        (stdout_value) = upload.communicate()
        successInfo = stdout_value[0]
        # errorInfo = stdout_value[1]
        if successInfo.__contains__('Already up to date') | successInfo.__contains__('file changed'):
            IILog().successPrint('### Git pull success.\n')
        else:
            IILog().failPrint('### Git pull fail....\n')
            exit()
        upload.wait()
    except Exception as e:
        # fail
        IILog().failPrint('### Git pull fails.\n')
        exit()

uploadIPAFile()