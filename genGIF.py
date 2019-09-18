# -*- coding:utf-8 -*-
import os

import imageio
import progressbar
from PIL import Image


def resizePic(fp, saveFp, width=None, height=None):
    # resize
    im = Image.open(fp)
    # name = saveFp.split('.')[0] + '.png'
    oriW, oriH = im.size
    if not height:
        height = int(oriH / oriW * width)
    if not width:
        width = int(oriW / oriH * height)

    out = im.resize((width, height), Image.ANTIALIAS)
    out.save(saveFp)


def genGif(picList, savePath, duration=0.033):
    path = os.path.join(savePath, 'noise.gif')
    imageio.mimsave(path, picList, 'GIF', duration=duration)


def main():
    cwd = 'E:\\Users\\acer\\Desktop\\noise2_redo\\'
    savePath = 'E:\\Users\\acer\\Desktop\\resize\\'
    picList = []
    dirList = os.listdir(cwd)
    length = len(dirList)
    # dirList1 = [dirList[2 * i] for i in range(length // 2)]
    dirList1 = []
    # dirList2 = []
    dirList2 = [dirList[4 * i] for i in range(length // 4)]
    dirList = dirList2 + dirList[-4:-1]
    for f in progressbar.progressbar(dirList):
        resizePic(cwd + f, savePath + f, height=300)
    dirSave = os.listdir(savePath)
    # dirSave = dirList2
    # savePath=cwd
    for d in progressbar.progressbar(dirSave):
        pic = imageio.imread(savePath + d)
        picList.append(pic)
    genGif(picList, cwd, 0.06)


if __name__ == '__main__':
    main()
