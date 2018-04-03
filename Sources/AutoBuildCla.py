#!/usr/bin/env python


import subprocess
from IILog import *
import os
import datetime

'''
    ==============================
    BUILD FUNCTIONS ::
    0: CREATE IPABUILD FOLDER 
    1: GET SOURCE FILE PATH 
    2: RUN BUILD & EXPORT ORDER
    SUCCESS !
    ==============================
'''
class AutoBuildCla(object):

    def __init__(self):
        pass

    def autoBuild(self):

        sourcePath = ''
        sourceName = ''
        ipaFileName = ''
        exportConfigureFile = ''

        fileHandle = open('sourcePathsourceipaName.txt', 'r')
        for lineInfo in fileHandle.readlines():
            if lineInfo.__contains__('#'):
                # nothing
                continue
            elif lineInfo.__contains__('SourcePath'):
                # path
                sourcePath = lineInfo[13:].strip('\n')
            elif lineInfo.__contains__('WorkSpaceN'):
                # workspace name
                sourceName = lineInfo[13:].strip('\n')
            elif lineInfo.__contains__('IPAFileNam'):
                # ipa name
                ipaFileName = lineInfo[13:].strip('\n')
            elif lineInfo.__contains__('ExportFpat'):
                # ipa name
                exportConfigureFile = lineInfo[13:].strip('\n')
            else:
                # nothing
                continue

        fileHandle.close()

        # create ipafile folder
        now = datetime.datetime.now()
        dateStr = now.strftime('%Y_%m_%d__%H_%M_%S')
        archivePath = sourcePath + '/BuildFileNoahShan/' + dateStr + '/'
        isExists = os.path.exists(archivePath)
        if isExists :
            pass
        else:
            os.makedirs(archivePath)

        # ipa build
        buildpath = 'xcodebuild archive -workspace ' +  sourceName + ' -scheme ' + ipaFileName + '' \
                    ' -configuration Release ' \
                    '-archivePath ' + archivePath + ipaFileName + ' -allowProvisioningUpdates';
        IILog().successPrint('### Build start - build order is :')
        IILog().successPrint(buildpath)
        build = subprocess.Popen(buildpath, shell=True, cwd=sourcePath)
        build.wait()
        IILog().successPrint('### Build the file succeed.\n')

        # ipa export
        exportOrder = 'xcodebuild -exportArchive ' \
                    '-archivePath ' + archivePath + ipaFileName +'.xcarchive ' \
                    '-exportPath ' + archivePath + ' ' \
                    '-exportOptionsPlist ' + exportConfigureFile + ' -allowProvisioningUpdates';
        IILog().successPrint('### Export start - export order is :')
        IILog().successPrint(exportOrder)
        #
        IILog().failPrint('### If alert \'xcodebuild[13774:528009] [MT] ........ \',don\'t worry wait a moment! ')
        build = subprocess.Popen(exportOrder, shell=True, cwd=sourcePath)
        build.wait()
        IILog().successPrint('### Export the ipa file succeed.\n')

        return archivePath + ipaFileName + '.ipa'


# AutoBuildCla().autoBuild()