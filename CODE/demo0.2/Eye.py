#
# _*_ coding:UTF-8 _*_

from ctypes import *
import ctypes
import time
from playsound import playsound
 
import random
 
from random import choice

from ctypes import windll
from PIL import Image
from PIL import ImageGrab
import cv2
import numpy
import pytesseract
import difflib 
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()
    
class Eye:
    def __init__(self,name="mizukiyuta"):
        print("Eye Class initial")
        self._MYNAME=name
        
    def img_grab(self,box,convert_mode):
       im = ImageGrab.grab(box)
       if(convert_mode!=None):
           im = im.convert(convert_mode)
       return im
   
    def img_process(self,image,threshold=215):
        def my_thresold(threshold):
            table = []
            for j in range(256):
                if j < threshold:
                    table.append(1)
                else:
                    table.append(0)
            return table
        table1 = my_thresold(threshold)   
        im = image.point(table1,'1')
        # 参数 保存截图文件的路径
        #im.save('zy.png')
        return im
