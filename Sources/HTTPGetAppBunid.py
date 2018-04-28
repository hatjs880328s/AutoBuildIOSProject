# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name       ：  HTTPGetAppBunid
   Description     ：
   Author          ：  Noah_Shan
   date            ：  2018/4/28
-------------------------------------------------
   Change Activity :   2018/4/28:
-------------------------------------------------
"""
__author__ = 'Noah_Shan'


import urllib2
import json
import os
from IILog import *


IILog().successPrint('### Start change bundle ID')

bunble_identifier = 'com.Inspur.sourceTxt7718'

# get the bundleID file
def getBundlePathFromConfigFile():
    bundlePath = ''
    fileHandle = open('sourcePathsourceipaName.txt','r')
    for eachline in fileHandle.readlines():
        if eachline.__contains__('BundlePath'):
            bundlePath = eachline[13:].strip('\n')
            break
        else:
            continue
    fileHandle.close()
    return bundlePath

def getPBXPathFromConfigFile():
    bundlePath = ''
    fileHandle = open('sourcePathsourceipaName.txt','r')
    for eachline in fileHandle.readlines():
        if eachline.__contains__('PbxproPath'):
            bundlePath = eachline[13:].strip('\n')
            break
        else:
            continue
    fileHandle.close()
    return bundlePath

# follow the url change bundleid
def changeCharacter(localurl,replacedStr):
    filehandle = open(localurl,'r+')
    alllines = filehandle.readlines()
    filehandle.close()

    newALLline = []
    isBundleLine = False
    for eachLine in alllines:
        if isBundleLine:
            newline = '	<string>' + replacedStr + '</string>\n'
            newALLline.append(newline)
            isBundleLine = False
        else:
            if eachLine.__contains__('CFBundleIdentifier'):
                isBundleLine = True
            else:
                pass
            newALLline.append(eachLine)

    fileHan = open(localurl,'w')
    fileHan.writelines(newALLline)
    fileHan.close()

def changePRODUCT_BUNDLE_IDENTIFIERInpbxFile(localurl,replacedStr):
    filehandle = open(localurl, 'r+')
    alllines = filehandle.readlines()
    filehandle.close()

    changeCount = 0
    newAllLine = []
    for eachLine in alllines:
        if changeCount < 2:
            # PRODUCT_BUNDLE_IDENTIFIER = com.Inspur.sourceTxt7719;
            if eachLine.__contains__('PRODUCT_BUNDLE_IDENTIFIER'):
                newline = '				PRODUCT_BUNDLE_IDENTIFIER = ' + replacedStr + ';\n'
                newAllLine.append(newline)
                changeCount += 1
            else:
                newAllLine.append(eachLine)
        else:
            newAllLine.append(eachLine)

    fileHan = open(localurl, 'w')
    fileHan.writelines(newAllLine)
    fileHan.close()


# use return dic change displayname
def changeNameWithDic(bundlePath):
    replaced = {'bundleID': ''}


# get paths
realBundlePath = getBundlePathFromConfigFile()
pbxPath = getPBXPathFromConfigFile()
# change bundle ids
changeCharacter(realBundlePath, bunble_identifier)
changePRODUCT_BUNDLE_IDENTIFIERInpbxFile(pbxPath, bunble_identifier)

IILog().successPrint('### Change bundle ID end.')