# -*- coding: utf-8 -*-
import sys
import os
import re
import shutil
import glob
import datetime
from PIL import Image
from PIL.ExifTags import TAGS
from tqdm import tqdm
import ffmpeg
import json

def get_exif(img,file):
    exif = img._getexif()
    try:
        for id,val in exif.items():
            tg = TAGS.get(id,id)
            if tg == "DateTimeOriginal":
                return val
    except AttributeError:
            if os.path.exists(file) :
                dt = datetime.datetime.fromtimestamp(os.stat(file).st_mtime)
                key = dt.strftime('%Y:%m:%d %H:%M:%S')
                return key
    if os.path.exists(file) :
        dt = datetime.datetime.fromtimestamp(os.stat(file).st_mtime)
        key = dt.strftime('%Y:%m:%d %H:%M:%S')
    return key
 
def list_files(dir,func):
    for file in dir:
        try:
            img = Image.open(file)
        except:
            continue
        datetimeinfo = func(img,file)
        yield (file, datetimeinfo)
        img.close()
 
def make_folda(taginfo):
    date_str = re.split(':|\s', taginfo[1])
    year = date_str[0]
    month = date_str[1]
    date = str(date_str[1]) + str(date_str[2])
    time = date_str[3] + '_'+ date_str[4] + '.'+ date_str[5]
    fd_path = '整理済み/写真/' + str(year) +'/'+ str(month)
    datetime = str(year) +'-'+ str(date) + '-' + str(time)
    os.makedirs(fd_path, exist_ok=True )
    return fd_path,datetime
 
def make_folda_douga(taginfo,datatimes):
    date_str = re.split(':|\s|-|T|\.', datatimes)
    year = date_str[0]
    month = date_str[1]
    date = str(date_str[1]) + str(date_str[2])
    time = date_str[3] + '_'+ date_str[4] + '.'+ date_str[5]
    fd_path = '整理済み/動画/' + str(year) +'/'+ str(month)
    datetimestr = str(year) +'-'+ str(date) + '-' + str(time)
    os.makedirs(fd_path, exist_ok=True )
    return fd_path, datetimestr


def find_metadata_atom(file, name):
       atom = file.find('.//%s//data' % name)
       return atom.get_attribute('data')


def getdatetimeinJSON(json_dict):
    if 'format' not in json_dict.keys():
        return None
    if 'tags' not in json_dict['format'].keys():
        return None
    if 'creation_time' not in json_dict['format']['tags'].keys():
        return None
    return json_dict['format']['tags']['creation_time']

def main():
    id = 0
    print("写真(jpg)の整理中")
    target_path = glob.glob('.\imgs\**\*.jpg', recursive=True)
    list_jpg = list_files(target_path,get_exif)
    bar = tqdm(total = len(target_path))
    for taginfo in list_jpg:
        mv_path, datetime = make_folda(taginfo)
        id = id + 1
        new_path = shutil.copy2(taginfo[0], mv_path + '/' +datetime+'_'+str(id) +'.jpg')
        bar.update(1)

    print("写真(png)の整理中")
    target_path_png = glob.glob('.\imgs\**\*.png', recursive=True)
    list_png = list_files(target_path_png,get_exif)
    bar = tqdm(total = len(target_path_png))
    list_png = list_files(target_path_png,get_exif)
    for taginfo in tqdm(list_png):
        mv_path, datetime = make_folda(taginfo)
        id = id + 1
        new_path = shutil.copy2(taginfo[0], mv_path + '/' +datetime+'_'+str(id) +'.png')
        bar.update(1)

    print("写真(HEIC)の整理中")
    target_path_heic = glob.glob('.\imgs\**\*.heic', recursive=True)
    list_png = list_files(target_path_heic,get_exif)
    bar = tqdm(total = len(target_path_heic))
    list_heic = list_files(target_path_heic,get_exif)
    for taginfo in tqdm(list_heic):
        mv_path, datetime = make_folda(taginfo)
        id = id + 1
        new_path = shutil.copy2(taginfo[0], mv_path + '/' +datetime+'_'+str(id) +'.heic')
        bar.update(1)


    print("動画(mp4)の整理中")
    target_path_mp4 = glob.glob('.\imgs\**\*.mp4', recursive=True)
    for path in tqdm(target_path_mp4):
        video_info = ffmpeg.probe(path)
        json_dict = json.loads(json.dumps(video_info))
        datatimes = getdatetimeinJSON(json_dict)
        mv_path, datetimestr = make_folda_douga(path,datatimes)
        id = id + 1
        new_path = shutil.copy2(path, mv_path + '/' +datetimestr+'_'+str(id) +'.mp4')

    print("動画(mov)の整理中")
    target_path_mov = glob.glob('.\imgs\**\*.mov', recursive=True)
    for path in tqdm(target_path_mov):
        try:
            video_info = ffmpeg.probe(path)
            json_dict = json.loads(json.dumps(video_info))
            datatimes = getdatetimeinJSON(json_dict)
            mv_path, datetimestr = make_folda_douga(path,datatimes)
            id = id + 1
            new_path = shutil.copy2(path, mv_path + '/' +datetimestr+'_'+str(id) +'.mov')
        except:
            print(path)



if __name__ == '__main__':
    main()