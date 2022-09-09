import requests as r
import subprocess as pr
import re, os, glob


def getFile():
    os.chdir('download')
    file = glob.glob("*.zip")
    file = 'download/'+file[0]
    os.chdir('../')
    return file


def downloadFile(url):
    pr.run(['rm','-r', 'download'])
    pr.run(['wget','-P','download', url])

def getVersion():
    res = r.get('https://github.com/ventoy/Ventoy/releases')
    x = re.search(r'ventoy-(\d+\.\d+\.\d+)-windows.zip:\s+(\S{64})', res.text)
    return x.group(1)


def getUrl(version):
    BASE_URL = 'https://github.com/'
    VENTOY_URL = 'ventoy/Ventoy/releases/download/v'
    VENTOY = '/ventoy-'
    FILE_URL = '-windows.zip'
    return BASE_URL+VENTOY_URL+version+VENTOY+version+FILE_URL


def checkVersion(version):
    with open('ventoy-version.txt') as file:
        oldVersion = file.read()

    if oldVersion != version:
        with open('ventoy-version.txt','w') as file:
            file.write(version)
        downloadFile(getUrl(getVersion()))

checkVersion(getVersion())