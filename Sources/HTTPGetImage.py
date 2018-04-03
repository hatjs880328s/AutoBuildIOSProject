#!/usr/bin/env python

import urllib2
import time
import json
import os
from IILog import *

'''
    First get All pic's url
    Second download all of them 
    Third save in directly folder
    #reference:
    <download pics>
    <read api     >
'''

IILog().successPrint('####### Start - HTTPGetImageModule---')
# get net work pic url
def loadALLPicsURL(url):
    picDic = {}
    # YSJ PIC
    picDefaulturl = 'http://chuxxxxcxxxx220.png'
    # CLOUD PIC
    picLandurl = 'http://chuaxxxxxxxxxxxx20.png'

    response = urllib2.urlopen(url)
    jsondata = json.loads(response.read())

    for eachItem in jsondata['result']:
        picDic[eachItem['id']] = picDefaulturl
    return picDic


# the api url is to get Some pics
def getAPIUrl():
    apiUrl = ''
    fileHandle = open('sourcePathsourceipaName.txt', 'r')
    for eachItem in fileHandle.readlines():
        if eachItem.__contains__('ApiRefurls'):
            apiUrl = eachItem[13:].strip('\n')
            break
        else:
            continue
    print('### The pics url is: ' + apiUrl)
    fileHandle.close()
    return apiUrl

# local pic path
def getLocalPicPath():
    logoPath = ''
    fileHandle = open('sourcePathsourceipaName.txt', 'r')
    for eachItem in fileHandle.readlines():
        if eachItem.__contains__('LogoRepath'):
            logoPath = eachItem[13:].strip('\n')
            break
        else:
            continue
    fileHandle.close()
    print('### The Local logo path is: ' + logoPath)
    return logoPath + '/'


'''
    GET URL THAT IT CAN GET PICS - apiUrl
    GET ALL PICS URL LIST<STRING> -  picUrls
'''

# pic api address
apiUrl = getAPIUrl()
# pic url dic <string,string>
picUrls = loadALLPicsURL(apiUrl)
# local logo path
localLogopath = getLocalPicPath()
IILog().successPrint('### Get all pic url & names ok...\n')


'''
    GET PIC DATA WITH PICURL
    GO-
'''
# get net pic & write to directly file
def getImageData(picName,picUrl):
    binary_data = urllib2.urlopen(picUrl).read()
    temp_file = open(picName, 'wb')
    temp_file.write(binary_data)
    temp_file.close()

# loop in - get all local logo path & use getImageData() function change it's data
def runloopChangePic():
    # for picValue in picDir.keys():
    path = localLogopath
    for file in os.listdir(path):
        if file.__contains__('.png'):
            print('### Change pic ' + file + ' data start...')
            getImageData(path + file, picUrls.values()[0])
            IILog().successPrint('### Change pic ' + file + ' data end...\n')



'''
    START-CHANGE LOGO DATA
'''
runloopChangePic()
IILog().successPrint('### Pics Change ok.')

