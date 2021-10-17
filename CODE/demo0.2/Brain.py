#
# _*_ coding:UTF-8 _*_

from ctypes import *
import ctypes
import time

print("[Load Eye Class...]")
import Eye
Eye_controller = Eye.Eye()

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
    
fish_pokemon_dict={"Feebas":0,
                   "Carvanha":0,
                   "Tentacool":0,
                   "Sharpedo":0,
                   "Magikarp":0}   
shiny_text_list=["shiny","hin","iny","ny","Shi","nyR"]

class Brain:
    def __init__(self,name="mizukiyuta"):
        print("Brain Class initial")
        self._MYNAME=name
    def get_equal_rate(self,str1, str2):
        return difflib.SequenceMatcher(None, str1, str2).quick_ratio()
   
    def Judge_text_info(self,text):
        print("[Judge_text_info...]")
        fish_pokemon_scores = fish_pokemon_dict 
        for key in fish_pokemon_scores.keys():
            fish_pokemon_scores[key] = self.get_equal_rate(key, text)
        print("fish or not score:",fish_pokemon_scores)
        max_score = max(zip(fish_pokemon_scores.values(), fish_pokemon_scores.keys()))
        #print(max_scores) # (0.5, 'B')
        if(max_score[0]<0.5):
            return "water",max_score
        else:
            return "battle",max_score
    def Judge_Feebas(self):
        is_feebas=False
        is_shiny=False
        box = (230,172,400,192)#pokemon name info
        im = Eye_controller.img_grab(box=box,convert_mode="L")
        im = Eye_controller.img_process(im)
        name_text=pytesseract.image_to_string(im)
        name_text = name_text.replace(' ', '').replace('\n','').replace('\t','')
        print("JUDGE_Feebas text is{",name_text,"}")
        scene,max_score = self.Judge_text_info(name_text)
        for item in shiny_text_list:
            if(item in name_text):
                 print("!"*50)
                 print("!!Shiny Pokemon!!!")
                 print("!"*50)
                 is_shiny=True
        if(max_score[1]=="Feebas"):
            is_feebas=True
        else:
            is_feebas=False
        return is_feebas,is_shiny
    
    def Judge_shiny(self):
        print("[Judge_shiny...]")
        box = (230,172,400,192)#pokemon name info
        im = Eye_controller.img_grab(box=box,convert_mode="L")
        im = Eye_controller.img_process(im)
        name_text=pytesseract.image_to_string(im)
        name_text = name_text.replace(' ', '').replace('\n','').replace('\t','')
        print("JUDGE_SHINY text is{",name_text,"}")
        for item in shiny_text_list:
            if(item in name_text):
                 print("!"*50)
                 print("!!Shiny Pokemon!!!")
                 print("!"*50)
                 return True
        print("JUDGE_SHINY result:{","not Shiny","False","}")
        return False

    def Judge_scene(self):
        print("[Judge_scene...]")
        box = (230,172,400,192)#pokemon name
        im = Eye_controller.img_grab(box=box,convert_mode="L")
        im = Eye_controller.img_process(image=im,threshold=215)
        
        name_text=pytesseract.image_to_string(im)
        name_text = name_text.replace(' ', '').replace('\n','').replace('\t','')
        print("JUDGE_SCENE text is{",name_text,"}")
        
        scene,max_score = self.Judge_text_info(name_text)
        print("JUDGE_SCENE scene is{",scene,"}")
        print("JUDGE_SCENE max_score is{",max_score,"}")
        return scene

