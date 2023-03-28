#!/bin/python

from requests import get
from subprocess import run
from glob import glob
from os import chdir
from re import search


def getFile():
    chdir('download')
    file = glob("*.zip")
    file = 'download/'+file[0]
    chdir('../')
    return file


def downloadFile(url):
    run(['rm','-rf', 'download'])
    run(['wget','-P','download', url])

def getVersion():
    res = get('https://github.com/ventoy/Ventoy/releases')
    x = search(r'ventoy-(\d+\.\d+\.\d+)-windows.zip:\s+(\S{64})', res.text)
    return x.group(1)


version = getVersion()
with open('ventoy-version.txt', 'w+') as file:
    if not file:
        file.write(version)
    elif file.read() != version:
        file.write(version)
        downloadFile(f'https://github.com/ventoy/Ventoy/releases/download/v{version}/ventoy-{version}-windows.zip')