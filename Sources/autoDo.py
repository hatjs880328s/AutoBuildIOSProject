#!/usr/bin/env python

import subprocess
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from IILog import *
from AutoBuildCla import *



IILog().successPrint('\n'
      '### Use python auto build & upload project \n'
      '### First build the ipa file,make sure the source folder has no ipa file\n'
      '### If exist deleate it(eg: icloud.ipa)\n'
      '### Second auto build the ipa & upload it \n'
      '### Ur job just wait\n'
      '### Ok,go-\n\n')

import HTTPGetImage
import HTTPGetAppname



'''
    ==============================
    BUILD FUNCTIONS
    ==============================
'''

print('####### Now build the xxx.ipa file----\n')

# progress source path & source name & Email-Receivers
sourcePath = ''
sourceName = ''
emailReceivers = []
ipaFilePath = ''

fileHandle = open('sourcePathsourceipaName.txt', 'r')
for lineInfo in fileHandle.readlines():
    if lineInfo.__contains__('#'):
        # nothing
        continue
    elif lineInfo.__contains__('SourcePath'):
        # path
        sourcePath = lineInfo[13:].strip('\n')
    elif lineInfo.__contains__('SourceName'):
        # name
        sourceName = lineInfo[13:].strip('\n')
    elif lineInfo.__contains__('EmailReces'):
        # Email-Receivers
        emailResult = lineInfo[13:].strip('\n').split(',')
        for eachItem in emailResult:
            if eachItem != '':
                emailReceivers.append(eachItem)
    else:
        # nothing
        continue

fileHandle.close()

# ipa build with [shenzhen]
# build = subprocess.Popen('ipa build', shell=True, cwd=sourcePath)
# build.wait()
# IILog().successPrint('### Build the ipa succeed.\n')
ipaFilePath = AutoBuildCla().autoBuild()



'''
    ==============================
    UPLOAD FUNCTIONS RETRY 3 TIMES
    ==============================
'''

# upload the ipa file with FIR.CLA
print('####### Now upload the ipa file to fir----')
print('### If alert \'One or more parameters passed to a function were not valid \' '
      'with Orange color characters don\'t worry,just wait...\n')

class uploadIns(object):
    # errInfo
    errUploadInfo = ''
    # successInfo
    successUploadInfo = ''
    # resultFlag
    ifSuccess = True
    # redo count max <= 3
    redoCount = 0


# path is -----  sourcePath + sourceName
def uploadIPAFile(path,redoTime):
    uploadInstanceIn = uploadIns()
    try:
        upload = subprocess.Popen(['fir', 'publish', path], stdout=subprocess.PIPE)
        (stdout_value) = upload.communicate()
        uploadInstanceIn.successUploadInfo = stdout_value[0]
        uploadInstanceIn.errUploadInfo = stdout_value[1]
        if uploadInstanceIn.successUploadInfo.__contains__('Published succeed'):
            # succeed
            uploadInstanceIn.ifSuccess = True
            IILog().successPrint('### Upload the file succeed.\n')
        else:
            # fail
            uploadInstanceIn.ifSuccess = False
            if redoTime <= 2:
                IILog().failPrint('### Upload the file fail, retring... \n')
                return uploadIPAFile(path,redoTime + 1)
            else:
                IILog().failPrint('### Upload the file fail.\n')
        upload.wait()
    except Exception as e:
        # fail
        uploadInstanceIn.ifSuccess = False
        if redoTime <= 2:
            IILog().failPrint('### Upload the file fail<catch exception>, retring... \n')
            return uploadIPAFile(path, redoTime + 1)
        else:
            IILog().failPrint('### Upload the file fail.\n')
    return uploadInstanceIn

# invoking the upload method (retry 3 times)
IILog().successPrint('### Upload ipa path is ' + ipaFilePath)
uploadInstance = uploadIPAFile(ipaFilePath,0)


'''
    ==============================
    E-MAIL FUNCTIONS BY CONFIG FILE 
    ==============================
'''

def isSuccessFunc(ifSuccess):
    resultstr = 'succeed!' if ifSuccess else 'Fail!'
    return resultstr


# send E-mail to Observer
emailSender = 'xxxx45552@qq.com'
emailContext = 'Auto build & upload ipa ' + isSuccessFunc(uploadInstance.ifSuccess) + ' \n \n \n ' \
               + '\n\nResultInfo:' + uploadInstance.successUploadInfo + '\n\n That\'s all.'
# mail instance
emailInstance = MIMEText(emailContext, 'plain', 'utf-8')
emailInstance['From'] = Header('iOSTeam', 'utf-8')
emailInstance['To'] = Header('observer', 'utf-8')
emailInstance['Subject'] = Header('iOS Upload IPA ' + isSuccessFunc(uploadInstance.ifSuccess), 'utf-8')
# smtp-server instance
mail_host = 'smtp.qq.com'
mail_port = '465'
mail_user = 'xxxx5552@qq.com'
mail_pass = 'xxxxxxxxxxx'
try:
    smtpOBJ = smtplib.SMTP_SSL(mail_host, mail_port)
    smtpOBJ.login(mail_user, mail_pass)
    smtpOBJ.sendmail(emailSender, emailReceivers, emailInstance.as_string())
    smtpOBJ.quit()
    IILog().successPrint('### E-mail send succeed...')
except smtplib.SMTPException:
    IILog().failPrint('### E-mail send fail...')
