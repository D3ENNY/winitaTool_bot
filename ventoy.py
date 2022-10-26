#!/bin/python

from requests import get
from subprocess import run
from glob import glob
from os import chdir
from re import search

def getFile():
    path = 'download/ventoy/'
    chdir(path)
    file = glob("*.zip")
    file = path+file[0]
    chdir('../../')
    return file


def downloadFile(url):
    run(['rm','-rf', 'download/ventoy'])
    run(['wget','-P','download/ventoy', url])

def getVersion():
    res = get('https://github.com/ventoy/Ventoy/releases')
    x = search(r'ventoy-(\d+\.\d+\.\d+)-windows.zip:\s+(\S{64})', res.text)
    return x.group(1)



    
print('---ventoy.py---')
version = getVersion()
# Watch out: garbage code ahead!
try:
    with open('version/ventoy-version.txt', 'r+') as file:
        if file.read() != version:
            file.truncate(0)
            file.write(version)
            downloadFile(f'https://github.com/ventoy/Ventoy/releases/download/v{version}/ventoy-{version}-windows.zip')

except FileNotFoundError:
    with open('version/ventoy-version.txt', 'w') as file:
        file.write(version)
        downloadFile(f'https://github.com/ventoy/Ventoy/releases/download/v{version}/ventoy-{version}-windows.zip')