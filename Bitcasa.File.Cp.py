#! -*- coding: utf-8 -*-
# Bitcasa.File.Cp.py
# 2014.02.09 K. Kuwata

import os
import glob
import shutil
import sys
from time import sleep

TransferSpeed = 5000000.0 # byte/sec

def ListDirectry(path):
    files = glob.glob(path + "/*")
    return files

def CheckFileDirectry(path):
    dic = {}
    if os.path.isdir(path):
        dic['type'] = 0
        dic['path'] = path
    elif os.path.isfile(path):
        dic['type'] = 1
        dic['path'] = path
    return dic

def fild_all_files(directory):
    for root, dirs, files in os.walk(directory):
        yield root
        for file in files:
            yield os.path.join(root, file)

def CreateDirectry(Dirpath):
    os.makedirs(Dirpath)

def ReturnRootpath(path):
    lis = path.split('/')
    while lis.count('') > 0:
        lis.remove('')
    rootpath = "/" + "/".join(lis[0:-1])
    return rootpath

def ReclusiveSearch(path, Dpath):
    rootpath = ReturnRootpath(path)
    Opath = fild_all_files(path)
    ListFPath = []
    for fl in Opath:
        fpath = CheckFileDirectry(fl)
        if fpath['type'] == 1:
            ListFPath.append(fpath['path'])
        elif fpath['type'] == 0:
            DirPath = fpath['path'].replace(rootpath, Dpath)
            CreateDirectry(DirPath)
    return ListFPath

def GetFileTransTime(fpath):
    filesize = float(os.path.getsize(fpath))
    ftime = filesize / TransferSpeed
    return ftime

def FilesCopy(path, Dpath):
    rootpath = ReturnRootpath(path)
    try:
        ListFpath = ReclusiveSearch(path,  Dpath)
    except:
        None
    N = len(ListFpath)
    n = 0
    for fpath in ListFpath:
        ftime = GetFileTransTime(fpath)
        Dfpath = fpath.replace(rootpath, Dpath)
        shutil.copyfile(fpath, Dfpath)
        n = n + 1
        percent = float(n) / float(N) * 100
        print("%.2f %% (%d/%d): Copy %s to %s\r" % \
                (percent, n, N, fpath, Dfpath))
        sleep(ftime)

def Execute():
    while True:
        try:
            path = raw_input("Please enter directry path which you want to copy into Bitcasa:\n")
            Dpath = raw_input("Please enter destination path in Bitcasa:\n")
            FilesCopy(path, Dpath)
            print "Finish copying!"
            break
        except:
            print "Oops! That was no valid. Try again..."


if __name__=='__main__':
    Execute()
