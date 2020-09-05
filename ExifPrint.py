import os
import re
import shutil
import glob
import datetime
from PIL import Image
from PIL.ExifTags import TAGS
from tqdm import tqdm

target_path = glob.glob('.\imgs\**\*.jpg', recursive=True)

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
    for file in target_path:
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
    fd_path = '整理済み/' + str(year) +'/'+ str(month)
    datetime = str(year) +'-'+ str(date) + '-' + str(time)
    os.makedirs(fd_path, exist_ok=True )
    return fd_path,datetime
 


def main():
    id = 0
    for taginfo in tqdm(list_files(target_path,get_exif)):
        mv_path, datetime = make_folda(taginfo)
        id = id + 1
        new_path = shutil.copy2(taginfo[0], mv_path + '/' +datetime+'_'+str(id) +'.jpg')

if __name__ == '__main__':
    main()