# -*- coding: utf-8 -*-
"""
Created on Mon Oct 18 19:25:33 2021

@author: mizukiyuta
"""
import pyautogui
from pynput.keyboard import Key, Controller
import cv2
from collections import Counter
import os,sys
sys.path.append(r'C:/Users/mizukiyuta/Desktop/pokemmo-mizuki/')    #要用绝对路径
#print(sys.path)        #查看模块路径
import mss
import numpy
import matplotlib.pyplot as plt
import time
import math
from PIL import Image
import scipy.misc
import matplotlib

import multiprocessing 

def read_img(img_category_name,img_num):
    img_list=[]
    w_list=[]
    h_list=[]
    for i in range(img_num):
        img_name=img_category_name+str(i)+".png"
        img = cv2.imread('./data/'+img_name, 0)
        img_list.append(img)
        w, h = img.shape[::-1]
        w_list.append(w)
        h_list.append(h)
    return img_list,w_list,h_list

#------------------------------------------------------
player_img_list,pw_list,ph_list=[],[],[]
N=5
player_img_list,pw_list,ph_list=read_img("player",N)
#------------------------------------------------------
dialog_img_list,dw_list,dh_list=[],[],[]
M=2
dialog_img_list,dw_list,dh_list=read_img("dialog",M)
#------------------------------------------------------  
sharpedo_img_list,sw_list,sh_list=[],[],[]
S=4
sharpedo_img_list,sw_list,sh_list=read_img("sharpedo",S)
#------------------------------------------------------
carvaha_img_list,cw_list,ch_list=[],[],[]
C=3
carvaha_img_list,cw_list,ch_list=read_img("carvaha",C)
#------------------------------------------------------
feebas_img_list,fw_list,fh_list=[],[],[]
F=4
feebas_img_list,fw_list,fh_list=read_img("feebas",F)
#------------------------------------------------------

global now_pokemon_name
now_pokemon_name="None"
now_scene_name=""
class Pokemmo_Detector:
    def __init__(self,name="mizukiyuta"):
        self._MYNAME=name
    def start_water_monitor(self,detect_num):
         with mss.mss() as sct:
            # Part of the screen to capture
           # monitor = {'top': 150, 'left': 760, 'width': 268, 'height':200}
            monitor = {'top': 50, 'left': 260, 'width': 900, 'height': 600}
            #monitor = {}
            i=0
            while 'Screen capturing':
                img = numpy.array(sct.grab(monitor))  
                img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                #cv2.rectangle(img, [300,60], (300 + 400, 60+150), (0, 0, 255), 2)
                res1_list=[]
                for i in range(N):
                    #res = cv2.matchTemplate(img_gray, player_img_list[i], cv2.TM_CCOEFF_NORMED)
                    res = cv2.matchTemplate(img_gray, player_img_list[i], cv2.TM_CCOEFF_NORMED)
                    res1_list.append(res)
                res2_list=[]
                for i in range(M):
                    #res = cv2.matchTemplate(img_gray, player_img_list[i], cv2.TM_CCOEFF_NORMED)
                    res = cv2.matchTemplate(img_gray, dialog_img_list[i], cv2.TM_CCOEFF_NORMED)
                    res2_list.append(res)

                    
                threshold = 0.64
                for j in range(N):
                    loc2 = numpy.where(res1_list[j] >= threshold)
                    for pt in zip(*loc2[::-1]):
                        cv2.rectangle(img, pt, (pt[0] + pw_list[j], pt[1] + ph_list[j]), (0, 0, 255), 2)

                threshold = 0.92
                for j in range(M):
                    loc2 = numpy.where(res2_list[j] >= threshold)
                    for dt in zip(*loc2[::-1]):
                        cv2.rectangle(img, dt, (dt[0] + dw_list[j], dt[1] + dh_list[j]), (0, 255, 0), 2)
                
                cv2.imshow('water_detector', img)
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()
                    break     
                
    def start_battle_monitor(self,detect_num):
         with mss.mss() as sct:
            # Part of the screen to capture
            monitor = {'top': 200, 'left': 600, 'width': 500, 'height': 200}
            Carvaha_num=0
            Sharpedo_num=0
            Feebas_num=0
            circle_num=0
            
            while 'Screen capturing':
                circle_num=circle_num+1
                img = numpy.array(sct.grab(monitor))  
                img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                #cv2.rectangle(img, [300,60], (300 + 400, 60+150), (0, 0, 255), 2)
                res2_list=[]
                for i in range(C):
                    #res = cv2.matchTemplate(img_gray, player_img_list[i], cv2.TM_CCOEFF_NORMED)
                    res = cv2.matchTemplate(img_gray, carvaha_img_list[i], cv2.TM_CCOEFF_NORMED)
                    res2_list.append(res)
                    
                res3_list=[]
                for i in range(S):
                    #res = cv2.matchTemplate(img_gray, player_img_list[i], cv2.TM_CCOEFF_NORMED)
                    res = cv2.matchTemplate(img_gray, sharpedo_img_list[i], cv2.TM_CCOEFF_NORMED)
                    res3_list.append(res)
                    
                res4_list=[]
                for i in range(F):
                    #res = cv2.matchTemplate(img_gray, player_img_list[i], cv2.TM_CCOEFF_NORMED)
                    res = cv2.matchTemplate(img_gray, feebas_img_list[i], cv2.TM_CCOEFF_NORMED)
                    res4_list.append(res)
                    
                    
                 
                has_Carvaha=False
                threshold = 0.68
                for j in range(C):
                    loc2 = numpy.where(res2_list[j] >= threshold)
                    for ft in zip(*loc2[::-1]):
                        has_Carvaha=True
                        Carvaha_num=Carvaha_num+1
                        cv2.rectangle(img, ft, (ft[0] + fw_list[j], ft[1] + fh_list[j]), (0,0,255), 2)
                if(has_Carvaha):
                    cv2.putText(img, 'Carvaha', ft, cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)
                   
                
                has_Sharpedo=False
                threshold = 0.76
                for j in range(S):
                    loc2 = numpy.where(res3_list[j] >= threshold)
                    for st in zip(*loc2[::-1]):
                        has_Sharpedo=True
                        Sharpedo_num=Sharpedo_num+1
                        cv2.rectangle(img, st, (st[0] + sw_list[j], st[1] + sh_list[j]), (255,0, 0), 2)
                if(has_Sharpedo):
                    cv2.putText(img, 'Sharpedo', st, cv2.FONT_HERSHEY_COMPLEX, 1, (255,0, 0), 2)
                

                has_Feebas=False
                threshold = 0.57
                for j in range(F):
                    loc2 = numpy.where(res4_list[j] >= threshold)
                    for ft in zip(*loc2[::-1]):
                        has_Feebas=True
                        Feebas_num=Feebas_num+1
                        cv2.rectangle(img, ft, (ft[0] + fw_list[j], ft[1] + fh_list[j]), (255,255, 0), 2)
                if(has_Feebas):
                    cv2.putText(img, 'Feebas', ft, cv2.FONT_HERSHEY_COMPLEX, 1, (255,255, 0), 2)
                
                global now_pokemon_name
                if(circle_num==1):
                    circle_num=0
                    if(Carvaha_num>Sharpedo_num and Carvaha_num>Feebas_num and Carvaha_num>0):
                        now_pokemon_name="Carvaha"
                    elif(Feebas_num>Sharpedo_num and Feebas_num>Carvaha_num and Feebas_num>0):
                        now_pokemon_name="Feebas"
                    elif(Sharpedo_num>Feebas_num and Sharpedo_num>Carvaha_num and Sharpedo_num>0):
                        now_pokemon_name="Sharpedo" 
                    elif(Sharpedo_num==Feebas_num and Sharpedo_num==Carvaha_num and Feebas_num!=0):
                        now_pokemon_name="Analyzing..."
                    else:
                        now_pokemon_name="None"
                        Carvaha_num=Sharpedo_num=Feebas_num=0
                    
                    #minus to zero in 3 seconds
                    total_num = Sharpedo_num+Carvaha_num+Feebas_num
                    minus_num = int(total_num/10)
                    if(Sharpedo_num>0):
                        Sharpedo_num=Sharpedo_num-minus_num-1
                    if(Carvaha_num>0):
                        Carvaha_num=Carvaha_num-minus_num-1
                    if(Feebas_num>0):
                        Feebas_num=Feebas_num-minus_num-1

                cv2.putText(img, now_pokemon_name, [10,23], cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)  
                cv2.putText(img, "S:"+str(Sharpedo_num), [10,46], cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)  
                cv2.putText(img, "C:"+str(Carvaha_num), [10,69], cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)  
                cv2.putText(img, "F:"+str(Feebas_num), [10,92], cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)  
                cv2.imshow('battle_pokemon_detector', img)
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()
                    break     


def print_global_variable(n):
    while(True):
        time.sleep(1)
        print(now_pokemon_name)
if __name__ == "__main__": 
    PD = Pokemmo_Detector()
    PD.start_battle_monitor(10)
    # creating processes 
    """p1 = multiprocessing.Process(target=PD.start_battle_monitor, args=(10, )) 
    p2 = multiprocessing.Process(target=PD.start_water_monitor, args=(10, )) 
    #p3 = multiprocessing.Process(target=print_global_variable, args=(10, )) 
    
    # starting process 1&2
    p1.start() 
    p2.start() 
    #p3.start()
    
    # wait until process 1&2 is finished 
    p1.join() 
    p2.join() 
    #qp3.join()"""
