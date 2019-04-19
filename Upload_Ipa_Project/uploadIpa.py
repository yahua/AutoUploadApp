
import requests
import os
import json
import sys
import firUpload as fir

uploadLog = None

def initConfig(folder):
    global iconPath
    iconPath = folder + '/' + 'Icon-1024.png'
    jsonFilePath = folder + '/' + 'upload.json'
    if os.path.exists(jsonFilePath) == False:
        print('there is not upload config, so don\'t upload ipa')
        return
    global emailDict
    with open(jsonFilePath, 'r') as load_f:
        emailDict = json.load(load_f)
    if emailDict is None:
        print('there is not upload config, so don\'t upload ipa')
        return

    global uploadOpen
    uploadOpen = emailDict.get('uploadOpen')
    global uploadPlatform
    uploadPlatform = emailDict.get('uploadPlatform')
    global allUploadPlatform
    allUploadPlatform = emailDict.get('uploadPlatformInfo')
    global ipaPath
    ipaPath = folder + '/' + emailDict.get('ipaName')


def parserPgyerUploadResult(jsonResult):
    resultCode = jsonResult['code']
    if resultCode == 0:
        downUrl = 'https://www.pgyer.com/' + jsonResult['data']['buildShortcutUrl']
        print("Upload Success")
        print("DownUrl is:" + downUrl)
        return downUrl, 'https://appicon.pgyer.com/image/view/app_icons/'+jsonResult['data']['buildIcon']
    else:
        print("Upload Fail!")
        print("Reason:"+jsonResult['message'])
        return None, None

def uploadIpaToPgyer(ipaPath, platformDict):

    print ("ipaPath:%s" % ipaPath)
    files = {'file': open(ipaPath, 'rb')}
    headers = {'enctype':'multipart/form-data'}
    payload = {'_api_key':platformDict.get('_api_key'),
             'buildInstallType':platformDict.get('buildInstallType'),
             'buildPassword':platformDict.get('buildPassword'),
             'buildUpdateDescription':platformDict.get('log'),
             'buildName':platformDict.get('buildName')}
    print(str(payload))
    print('uploading....')
    r = requests.post(platformDict.get('uploadUrl'), data=payload, files=files, headers=headers)
    print(str(r))
    if r.status_code == requests.codes.ok:
        result = r.json()
        #print('result:%s' % result)
        return parserPgyerUploadResult(result)
    else:
        print('HTTPError,Code:'+r.status_code)
        return None, None
def notifyToDingDing(downloadUrl, picUrl):

    if (emailDict.get('notifyToDingDing') == '0'):
        return

    url = emailDict.get('dingdingUrl')
    content = '版本：' + allUploadPlatform.get(uploadPlatform).get('ipa_version') + \
              '\n更新内容：' + allUploadPlatform.get(uploadPlatform).get('log')
    data = {'msgtype': 'link',
            'link': {
                'title': 'app包新鲜出炉了！！！',
                'text': content,
                'messageUrl': downloadUrl,
                'picUrl': picUrl
                }
            }

    header = {'Content-Type': 'application/json'}
    data = json.dumps(data)
    res = requests.post(url, data=data, headers=header)
    print('钉钉通知')
    print(res.text)

def uploadIpa():
    if uploadOpen == '0':
        print('无法上传ipa，因为upload.json中uploadOpen为0')
        return
    if ipaPath is None:
        print('error ipaPath')
        return
    if uploadPlatform is None or uploadPlatform == '':
        print('not config uploadPlatform')
        return
    platformDict = allUploadPlatform.get(uploadPlatform)
    if platformDict is None or platformDict == '':
        print('can not find %s platform' % uploadPlatform)
        return
    if uploadPlatform == 'payer':
        downUrl, picUrl = uploadIpaToPgyer(ipaPath, platformDict)
        notifyToDingDing(downUrl, picUrl=picUrl)
        return
    if uploadPlatform == 'fir':
        downUrl, picUrl = fir.uploadIpaToFir(ipaPath, iconPath, platformDict)
        notifyToDingDing(downUrl, picUrl=picUrl)
        return


if __name__ == '__main__':

    dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))
    if dirname is None:
        print('请输入要打包的项目配置json路径')
    else:
        initConfig(dirname)
        uploadIpa()
