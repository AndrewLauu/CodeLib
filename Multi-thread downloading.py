# -*- coding:utf-8 -*-
import os
import threading
from contextlib import closing

import maya
import progressbar as p
import requests


def getRange(url, num):
    headers = requests.get(url, stream=True).headers
    fileSize = int(headers['content-length'])
    print(f'File size: {fileSize}')
    partSize = fileSize // num
    ranges = []
    for i in range(num):
        if i != num - 1:
            partRange = (i * partSize, (i + 1) * partSize - 1, partSize)
        else:
            partRange = (i * partSize, fileSize - 1, fileSize - (i - 2) * partSize)
        ranges.append(partRange)
    print(ranges)
    return ranges

def downloadFile(start, end, count, partSize):
    print(threading.currentThread())
    global downloadUrl
    widgets = [
        p.FileTransferSpeed(prefixes=('Ki', 'Mi')),
        p.Bar(left=' |', marker='>', fill='-', right='|'),
        p.DataSize(prefixes=('Ki', 'Mi')), ' (', p.Percentage(), ')| ',
        p.ETA()
    ]
    requestHeaders = {'Accept-Encoding': '*', 'Range': f'Bytes={start}-{end}'}
    tempFile = requests.get(downloadUrl, headers=requestHeaders, stream=True)  # .content
    tempFileName = f'E:\\Users\\acer\\Desktop\\pydl.pdf.{count}'
    # with closing(tempFile) as re:
    chunk = 1024  # B
    # count = 0
    # fileSize = fileSize / 1024  # KiB
    print(f'Downloading {tempFileName} from {downloadUrl}\nFile size: {partSize/1024/1024} MiB.')
    with open(tempFileName, 'wb') as f:
        for data in p.progressbar(tempFile.iter_content(chunk_size=chunk), max_value=partSize,
                                  widgets=widgets):  # ,prefix='* ', suffix=' #'):
            # f.seek(start)
            f.write(data)
            # count += 1

    # lock = threading.Lock()
    # print(fileName)
    # with open(fileName, 'wb') as f:
    #     # with lock:
    #     f.seek(start)
    #     f.write(epub.content)


def handleThread(ranges):
    count = 0
    threadList = []
    for item in ranges:
        print(item)
        start, end, partSize = item
        thread = threading.Thread(target=downloadFile, args=(start, end, count, partSize))
        threadList.append(thread)
        thread.start()
        # thread.join()
        count += 1
    for i in threadList:
        i.join()


def integrate(fileNumber):
    for i in range(fileNumber):
        tempFile = f'E:\\Users\\acer\\Desktop\\pydl.pdf.{i}'
        print(tempFile)
        with open(tempFile, 'rb') as dl:
            piece = dl.readlines()
            with open('E:\\Users\\acer\\Desktop\\pydl.pdf', 'ab+') as f:
                f.writelines(piece)
    for i in range(fileNumber):
        tempFile = f'E:\\Users\\acer\\Desktop\\pydl.pdf.{i}'
        os.remove(tempFile)


if __name__ == '__main__':
    startTime = maya.now()

    threadNum = 5  # Number of threads
    downloadUrl = 'https://raw.githubusercontent.com/nailperry-zd/The-Economist/master/2017-06-03/The_Economist_-_2017-06-03.pdf'
    ranges = getRange(downloadUrl, threadNum)
    handleThread(ranges)
    integrate(threadNum)
    endTime = maya.now()
    interval = endTime - startTime
    print(str(interval.seconds) + 's')
