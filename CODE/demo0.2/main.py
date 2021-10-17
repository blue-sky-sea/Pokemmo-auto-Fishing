#
# _*_ coding:UTF-8 _*_
import os,sys
sys.path.append(r'C:/Users/mizukiyuta/Desktop/pokemon-rose/')    #要用绝对路径
#print(sys.path)        #查看模块路径
from ctypes import *
import ctypes
import time

import pygame
pygame.init()

import random
 
from random import choice

from ctypes import windll
from PIL import Image
from PIL import ImageGrab


import Move,Brain
print("[Load Move,Brain Class...]")
brain_controller = Brain.Brain("mizukiyuta")
move_controller = Move.Move("mizukiyuta")
"""
from Eye import Eye_Class
from Move import Move_Class
from Brain import Brain_Class"""

def prepare_info():
    print("#"*50)
    print("Start fishing,please click to Pokemmo's window")
    time.sleep(4)
    print("...Start fishing!")  
    print("#"*50)
    print()
          
def do_fish():

    while(True):
        scene = brain_controller.Judge_scene()#on battle or on water
        if(scene=="battle"):
            is_shiny = brain_controller.Judge_shiny()
            if(is_shiny==False):
                print("No shiny,run")
                time.sleep(1)
                move_controller.run_from_battle(360,385)
                time.sleep(1)
            else:
                song = pygame.mixer.Sound("M09.ogg")
                song.play()
                time.sleep(1000)
            pass
        elif(scene=="water"):
            move_controller.do_a_fish(fish_key="i",confirm_key="j")
            pass
        else:
            time.sleep(5)
            continue
        print()
        
def find_fish():
     point_fish__counter=0
     while(True):
        scene = brain_controller.Judge_scene()#on battle or on water
        if(scene=="battle"):
            is_feebas,is_shiny = brain_controller.Judge_Feebas()
            if(is_feebas ==True):
                print("Find fish spot!")
                song = pygame.mixer.Sound("M09.ogg")
                song.play()
                break
            else:
                point_fish__counter=point_fish__counter+1
            if(is_shiny==False):
                print("No shiny,run")
                time.sleep(1)
                move_controller.run_from_battle(360,385)
                time.sleep(1)
            else:
                song = pygame.mixer.Sound("M09.ogg")
                song.play()
                time.sleep(1000)
            pass
        elif(scene=="water"):
            if(point_fish__counter>=3):
                move_controller.key_input(str="a")#go left
                point_fish__counter=0
            move_controller.do_a_fish(fish_key="i",confirm_key="j")
            pass
        else:
            time.sleep(5)
            continue
        print()   

if __name__ == "__main__":
    prepare_info()
    do_fish()
    find_fish()
    do_fish()