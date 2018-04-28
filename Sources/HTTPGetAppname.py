#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import json
import os
from IILog import *

'''
    The file should change the APP name with network
    User submit the name to remote server
    We get the app name from the remote server
'''
IILog().successPrint('\n\n####### Start - HTTPGetAppNameModule---')
class APPNameURL(object):
    # remote server api address
    nameURL = ''
    # local app name en path
    appnameEnpath = ''
    # local app name han-sim
    appnameHansim = ''
    # local app name han-tra
    appnameHantra = ''

# get the api url
def getURLFromConfigFile():
    appInstance = APPNameURL()
    fileHandle = open('sourcePathsourceipaName.txt','r')
    for eachline in fileHandle.readlines():
        if eachline.__contains__('AppNameURL'):
            appInstance.nameURL = eachline[13:].strip('\n')
        elif eachline.__contains__('AppnameEng'):
            appInstance.appnameEnpath = eachline[13:].strip('\n')
        elif eachline.__contains__('AppnameZHS'):
            appInstance.appnameHansim = eachline[13:].strip('\n')
        elif eachline.__contains__('AppnameZHT'):
            appInstance.appnameHantra = eachline[13:].strip('\n')
        else:
            continue
    fileHandle.close()
    return appInstance

# get the app names [return value type is DIC<string,string>]
def getAPPNamesWithURL(url):
    picDic = {}
    response = urllib2.urlopen(url)
    jsondata = json.loads(response.read())

    for eachItem in jsondata['result']:
        picDic[eachItem['id']] = 'customName'
    return picDic

# follow the url change displayname
def changeCharacter(localurl,replacedStr):
    filehandle = open(localurl,'r+')
    alllines = filehandle.readlines()
    filehandle.close()

    newALLline = []
    for eachLine in alllines:
        if eachLine.__contains__('CFBundleDisplayName'):
            newline = 'CFBundleDisplayName = ' + '\"' + replacedStr + '\";'
            newALLline.append(newline)
        else:
            newALLline.append(eachLine)
    fileHan = open(localurl,'w')
    fileHan.writelines(newALLline)
    fileHan.close()

# use return dic change displayname
def changeNameWithDic(dicValue,obj):
    replaced = {'AppnameEng': 'come', 'AppnameZHS': '醉了', 'AppnameZHT': '呵呵1'}
    changeCharacter(obj.appnameEnpath, replaced['AppnameEng'])
    changeCharacter(obj.appnameHansim, replaced['AppnameZHS'])
    changeCharacter(obj.appnameHantra, replaced['AppnameZHT'])



'''
    START CHANGE
'''
print('\n### Start change APP name....\n')
# get local path & name remote server path
appNameInstance = getURLFromConfigFile()
# get names use nameAPI
resultDic = getAPPNamesWithURL(appNameInstance.nameURL)
# change names
changeNameWithDic(resultDic, appNameInstance)
IILog().successPrint('### Change APP name ok\n')





