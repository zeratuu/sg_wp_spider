#!/usr/bin/env python
#coding: utf8
import os

import math
import random


def set_wallpaper(picpath):
    # curpath = commands.getstatusoutput('gsettings get org.gnome.desktop.background picture-uri')[1][1:-1]
    # if curpath == picpath:
    #     pass
    # else:
    # os.system('gsettings set org.gnome.desktop.background picture-uri "%s"' % (picpath))
    os.system('DISPLAY=:0 gsettings set org.gnome.desktop.background picture-uri "%s"' % (picpath))


# set_wallpaper("file:///media/wuhao/56C21FD8C21FBAE7/sg_wp_spider/0/765191.jpg")

# list=os.listdir("./")
# print(os.path.curdir)
# for i in list:
#     print(i)
def autoChange():
    imgfiles = []
    dir = "/home/wuhao/PycharmProjects/sg_wp_spider"
    for root, dirs, files in os.walk(dir):
        # print(len(files))
        # randint = random.randint(0, len(files) - 1)
        # imgfile="file://"+os.path.join(root,files[randint])
        for file in files:
            # print(os.path.join(root, file))
            if ".jpg" in file:
                imgfiles.append(os.path.join(root, file))
                # imgfiles.append('1')

    randint = random.randint(0, len(imgfiles) - 1)
    imgfile = "file://" + str(imgfiles[randint])
    set_wallpaper(imgfile)

if __name__ == '__main__':
    # cron
    autoChange()
