#!/bin/python

from requests import get
from subprocess import run
from glob import glob
from os import chdir
from re import search

def getFile():
    path = 'download/rufus/'
    chdir(path)
    file = glob("*.exe")
    file = path+file[0]
    chdir('../../')
    return file

def downloadFile(url):
    run(['rm', '-rf', 'download/rufus'])
    run(['wget','-P','download/rufus/', url])

def getVersion():
    res = get('https://rufus.ie/it/#')
    x = search(r'Rufus (\d.\d\d)', res.text)
    return x.group(1)

print('---rufus.py---')
version = getVersion()

try:
    with open('version/rufus-version.txt', 'rw') as file:
        if file.read() != version:
            file.write(version)
            downloadFile(f'https://github.com/pbatard/rufus/releases/download/v{version}/rufus-{version}.exe')
except FileNotFoundError:
    with open('ventoy-version.txt', 'w') as file:
        file.write(version)
        downloadFile(f'https://github.com/pbatard/rufus/releases/download/v{version}/rufus-{version}.exe')