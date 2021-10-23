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
from scipy.spatial.distance import pdist, squareform
import Brain
Brain_controller = Brain.Brain()
import Move,Brain
print("[Load Move,Brain,Detect Class...]")
Move_controller = Move.Move("mizukiyuta")

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
        img = cv2.imread('./data2/'+img_name, 0)
        img_list.append(img)
        w, h = img.shape[::-1]
        w_list.append(w)
        h_list.append(h)
    return img_list,w_list,h_list

#------------------------------------------------------
group_img_list,gw_list,gh_list=[],[],[]
G=5
group_img_list,gw_list,gh_list=read_img("group",G)
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
S=7
sharpedo_img_list,sw_list,sh_list=read_img("sharpedo",S)
#------------------------------------------------------
carvaha_img_list,cw_list,ch_list=[],[],[]
C=7
carvaha_img_list,cw_list,ch_list=read_img("carvaha",C)
#------------------------------------------------------
feebas_img_list,fw_list,fh_list=[],[],[]
F=9
feebas_img_list,fw_list,fh_list=read_img("feebas",F)
#------------------------------------------------------
shiny_img_list,shw_list,shh_list=[],[],[]
SH=1
shiny_img_list,shw_list,shh_list=read_img("Shiny",SH)
#------------------------------------------------------

global now_pokemon_name
now_pokemon_name="None"

global now_scene_name
now_scene_name="None"##water or battle


def delete_same_point(point_list,threshold=15):
    r=squareform(pdist(point_list))
    #print(r)
    need_to_delete_i=[]
    for i in range(len(r)):
        #i 0~6
        dis= r[i]
        if(i in need_to_delete_i):
            continue
        for d in range(len(dis)):
            #d 0~6
            if(dis[d]<threshold and d!=i):
                need_to_delete_i.append(d)
                
    #print(need_to_delete_i) 
    new_point_list=[]
    for i in range(len(point_list)):
        if(i not in need_to_delete_i):
            new_point_list.append(point_list[i])
    return new_point_list
class Pokemmo_Detector:
    def __init__(self,name="mizukiyuta"):
        self._MYNAME=name
    def getMoveCode(self,move):
        move_code=""
        move_name=move[0]
        move_dic={"Left":"a","Right":"d","Up":"w","Down":"s","Stop":""}
        return move_dic[move_name]
    def getNextMove(self,goalx,goaly):
        x=goalx
        y=goaly
        position="Other"
        next_move=["Stop"]
        #print("(370-x):",(370-x),"  (345-y):",(345-y))
        #在同一列上，x之间的差距不超过20
        if(abs(370-x)<=20):
            if((345-y)>100 and (345-y)<145):
                print((345-y),"On Fishing pot Down",(370-x))
                position="Down"
                next_move=["Stop"]
            elif((345-y)<-50):
                next_move=["Down"]
            elif((345-y)>155):
                next_move=["Up"]
            elif((345-y)<30 and (345-y)>-30):
                print((345-y),"On Fishing pot Up",(370-x))
                next_move=["Stop"]
        #在左边同一列上
        elif((370-x)<-50 and (370-x)>-80):
            #print("On left")
            if((345-y)<70 and (345-y)>40):
                print((345-y),"On Fishing pot Left",(370-x))
                position="Left"
                next_move=["Stop"]
            elif(((345-y))>100):
                next_move=["Right"]
            elif((345-y)<30 and (345-y)>-30):
                next_move=["Right"]
            elif((345-y)<-50):
                next_move=["Down"]
                
            pass
        #在右边同一列上     
        elif((370-x)>50 and (370-x)<80):
            #print("On Right")
            if((345-y)<70 and (345-y)>40):
                print((345-y),"On Fishing pot Right",(370-x))
                position="Right"
                next_move=["Stop"]
            elif(((345-y))>100):
                next_move=["Left"]
            elif((345-y)<30 and (345-y)>-30):
                next_move=["Left"]
            elif((345-y)<-50):
                next_move=["Down"]
            pass
        #在左边较远处
        elif((370-x)<-100):
            next_move=["Right"]
            pass
        #在右边较远处
        elif(((370-x)>100)):
            next_move=["Left"]
            pass
        return next_move,position      
    def start_pokemmo_monitor(self):
        n=0
        img=None
        title="None"
        
        with mss.mss() as sct:
            
            monitor = {'top': 50, 'left': 260, 'width': 780, 'height': 560}
            
            while 'Screen capturing':
                if(n%15==0):
                    scene = Brain_controller.Judge_scene()

                if(scene=="water"):
                    img,have_dialog,have_player,have_group,position,next_move = self.detect_water_player_dialog(sct,monitor,1)
                    print("[ONWATER]","dialog:",have_dialog,"player:",have_player,"group",have_group)
                    if(have_dialog==True):
                        #按下确定键后等待6秒
                        Move_controller.key_input(str="j")
                        time.sleep(6.5)
                    if(have_dialog==False and have_group==True):
                        move_code = self.getMoveCode(next_move)
                        Move_controller.key_input(str=move_code)
                        print("press key ",move_code)
                        time.sleep(6.5)
                    
                elif(scene=="battle"):                  
                    img,has_Carvaha,has_Sharpedo,has_Feebas= self.detect_battle_pokemon(sct,monitor,1)
                    #print("[BATTLE]","Carvas:",has_Carvaha,"Sharpedo",has_Sharpedo,"Feebas",has_Feebas)
                #cv2.imshow("test", img)
                n=n+1
                if cv2.waitKey(15) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()
                    break              
    def detect_water_player_dialog(self,sct,monitor,detect_num):
        have_dialog,have_player,have_group=False,False,False
        have_group_key1,have_group_key2=False,False
        position="Other"
        next_move=[]
        for i in range(detect_num):
            img = numpy.array(sct.grab(monitor))  
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            #cv2.rectangle(img, [300,60], (300 + 400, 60+150), (0, 0, 255), 2)
            res0_list=[]
            for i in range(G):
                #res = cv2.matchTemplate(img_gray, player_img_list[i], cv2.TM_CCOEFF_NORMED)
                res = cv2.matchTemplate(img_gray, group_img_list[i], cv2.TM_CCOEFF_NORMED)
                res0_list.append(res)
                
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
            
            group_points=[]
            threshold = 0.76
            for j in range(G):
                loc2 = numpy.where(res0_list[j] >= threshold)
                for pt in zip(*loc2[::-1]):
                    have_group_key1=True
                    cv2.rectangle(img, pt, (pt[0] + gw_list[j], pt[1] + gh_list[j]), (255, 0, 0), 2)
                    center_x = round((pt[0]+0.5*gw_list[j])/10)*10
                    center_y = round((pt[1]+0.5*gh_list[j])/10)*10
                    
                    
                    group_points.append([center_x,center_y])
            new_group_points=[]    
            if(len(group_points)>0):
                new_group_points = delete_same_point(group_points,15)
                 
            player_points=[]
            threshold = 0.64
            for j in range(N):
                loc2 = numpy.where(res1_list[j] >= threshold)
                for pt in zip(*loc2[::-1]):
                    have_player=True
                    cv2.rectangle(img, pt, (pt[0] + pw_list[j], pt[1] + ph_list[j]), (0, 0, 255), 2)
                    center_x = round((pt[0]+0.5*pw_list[j])/10)*10
                    center_y = round((pt[1]+0.5*ph_list[j])/10)*10
                    player_points.append([center_x,center_y])
                    #print(pw_list[j],ph_list[j])#73 28 / 67 31
                    #input()
            #删除 player_points中实际上就是同一个点的数据
            new_player_points=[]
            if(len(player_points)>0):
                new_player_points = delete_same_point(player_points,15)
            
            cv2.rectangle(img, (370-10,345-10), (370+10 ,345+10 ), (0, 255, 255), 2)
            if(len(new_player_points)<=5 and len(new_player_points)>=2):
                #print("group:",new_group_points)
                #print("player:",new_player_points)
                #求点集的中点
                def get_average_position(points):
                    total_x=0
                    total_y=0
                    for i in range(len(points)):
                        total_x = total_x+points[i][0]
                        total_y = total_y+points[i][1]
                    average_x=int(total_x/len(new_player_points))
                    average_y=int(total_y/len(new_player_points))
                    return average_x,average_y
                aver_x1,aver_y1 = get_average_position(new_player_points)
                aver_x2,aver_y2=aver_x1,aver_y1
                
                if(len(new_group_points)!=0):
                    aver_x2,aver_y2 = get_average_position(new_group_points)
                
                aver_x =  int((aver_x1+aver_x2)/2)
                aver_y =  int((aver_y1+aver_y2)/2)
                cv2.rectangle(img, (aver_x-10,aver_y-10), (aver_x+10 ,aver_y+10 ), (255, 255, 255), 2)
                
                
                if(len(new_group_points)>=1):
                    ##
                    x=new_group_points[0][0]
                    y=new_group_points[0][1]
                    #print("(370-x):",(370-x),"  (345-y):",(345-y))
                    next_move,position = self.getNextMove(x,y)
                elif(len(new_group_points)==0):
                    x=aver_x1
                    y=aver_y1
                    next_move,position = self.getNextMove(x,y)
                print(position,next_move)
            #print(new_player_points)
            #input("#"*30)
            #判断是否有三角或者四角    
            threshold = 0.92
            for j in range(M):
                loc2 = numpy.where(res2_list[j] >= threshold)
                for dt in zip(*loc2[::-1]):
                    have_dialog=True
                    cv2.rectangle(img, dt, (dt[0] + dw_list[j], dt[1] + dh_list[j]), (0, 255, 0), 2)
        
        
        return img,have_dialog,have_player,have_group ,position,next_move
       
    def detect_battle_pokemon(self,sct,monitor,detect_num):     
        img = numpy.array(sct.grab(monitor))  
        #img_gray=img
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
        threshold = 0.60
        for j in range(C):
            loc2 = numpy.where(res2_list[j] >= threshold)
            for ft in zip(*loc2[::-1]):
                has_Carvaha=True
                cv2.rectangle(img, ft, (ft[0] + fw_list[j], ft[1] + fh_list[j]), (0,0,255), 2)
        
        if(has_Carvaha):
            cv2.putText(img, 'Carvaha', ft, cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)
        
        has_Sharpedo=False
        threshold = 0.60
        for j in range(S):
            loc2 = numpy.where(res3_list[j] >= threshold)
            for st in zip(*loc2[::-1]):
                has_Sharpedo=True
                cv2.rectangle(img, st, (st[0] + sw_list[j], st[1] + sh_list[j]), (255,0, 0), 2)
        
        has_Feebas=False
        threshold = 0.58
        for j in range(F):
            loc2 = numpy.where(res4_list[j] >= threshold)
            for ft in zip(*loc2[::-1]):
                has_Feebas=True
                cv2.rectangle(img, ft, (ft[0] + fw_list[j], ft[1] + fh_list[j]), (255,255, 0), 2)
 
        if(has_Sharpedo):
            cv2.putText(img, 'Sharpedo', st, cv2.FONT_HERSHEY_COMPLEX, 1, (255,0, 0), 2)
        
        return img,has_Carvaha,has_Sharpedo,has_Feebas
    def start_water_monitor(self,conn_recv):
         with mss.mss() as sct:
            # Part of the screen to capture
           # monitor = {'top': 150, 'left': 760, 'width': 268, 'height':200}
            monitor = {'top': 50, 'left': 260, 'width': 780, 'height': 560}
            #monitor = {}
            i=0
            player_num=0
            dialog_num=0
            #circle_num=0
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

                    
                threshold = 0.62
                for j in range(N):
                    loc2 = numpy.where(res1_list[j] >= threshold)
                    for pt in zip(*loc2[::-1]):
                        player_num=player_num+1
                        cv2.rectangle(img, pt, (pt[0] + pw_list[j], pt[1] + ph_list[j]), (0, 0, 255), 2)

                threshold = 0.92
                for j in range(M):
                    loc2 = numpy.where(res2_list[j] >= threshold)
                    for dt in zip(*loc2[::-1]):
                        dialog_num=dialog_num+1
                        cv2.rectangle(img, dt, (dt[0] + dw_list[j], dt[1] + dh_list[j]), (0, 255, 0), 2)
                        
                pokemon_name = conn_recv.recv()
                cv2.putText(img, pokemon_name, [10,30], cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)  
               
                cv2.imshow('water_detector', img)
                
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()
                    break              
    def start_battle_monitor(self,conn_send):
         with mss.mss() as sct:
            # Part of the screen to capture
            monitor = {'top': 200, 'left': 600, 'width': 500, 'height': 200}
            Shiny_num=0
            Carvaha_num=0
            Sharpedo_num=0
            Feebas_num=0
            circle_num=0
            
            while 'Screen capturing':
                circle_num=circle_num+1
                img = numpy.array(sct.grab(monitor))  
                #img_gray=img
                img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                #cv2.rectangle(img, [300,60], (300 + 400, 60+150), (0, 0, 255), 2)
                res1_list=[]
                for i in range(SH):
                    #res = cv2.matchTemplate(img_gray, player_img_list[i], cv2.TM_CCOEFF_NORMED)
                    res = cv2.matchTemplate(img_gray, shiny_img_list[i], cv2.TM_CCOEFF_NORMED)
                    res1_list.append(res)
                    
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
                
                has_Shiny=False
                threshold = 0.82
                for j in range(SH):
                    loc2 = numpy.where(res1_list[j] >= threshold)
                    for sht in zip(*loc2[::-1]):
                        has_Shiny=True
                        Shiny_num=Shiny_num+1
                        cv2.rectangle(img, sht, (sht[0] + shw_list[j], sht[1] + shh_list[j]), (0,0,255), 2)
                if(has_Shiny):
                    cv2.putText(img, 'Shiny', sht, cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)
                   
                    
                has_Carvaha=False
                threshold = 0.60
                for j in range(C):
                    loc2 = numpy.where(res2_list[j] >= threshold)
                    for ft in zip(*loc2[::-1]):
                        has_Carvaha=True
                        Carvaha_num=Carvaha_num+1
                        cv2.rectangle(img, ft, (ft[0] + fw_list[j], ft[1] + fh_list[j]), (0,0,255), 2)
                if(has_Carvaha):
                    cv2.putText(img, 'Carvaha', ft, cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)
                   
                
                has_Sharpedo=False
                threshold = 0.60
                for j in range(S):
                    loc2 = numpy.where(res3_list[j] >= threshold)
                    for st in zip(*loc2[::-1]):
                        has_Sharpedo=True
                        Sharpedo_num=Sharpedo_num+1
                        cv2.rectangle(img, st, (st[0] + sw_list[j], st[1] + sh_list[j]), (255,0, 0), 2)
                if(has_Sharpedo):
                    cv2.putText(img, 'Sharpedo', st, cv2.FONT_HERSHEY_COMPLEX, 1, (255,0, 0), 2)
                

                has_Feebas=False
                threshold = 0.58
                for j in range(F):
                    loc2 = numpy.where(res4_list[j] >= threshold)
                    for ft in zip(*loc2[::-1]):
                        has_Feebas=True
                        Feebas_num=Feebas_num+1
                        cv2.rectangle(img, ft, (ft[0] + fw_list[j], ft[1] + fh_list[j]), (255,255, 0), 2)
                if(has_Feebas):
                    cv2.putText(img, 'Feebas', ft, cv2.FONT_HERSHEY_COMPLEX, 1, (255,255, 0), 2)
                
                global now_pokemon_name
                try:
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
                    if(circle_num%10==0):
                        conn_send.send(now_pokemon_name)

                    #minus to zero in 3 seconds
                    total_num = Sharpedo_num+Carvaha_num+Feebas_num
                    minus_num = int(total_num/10)
                    if(Sharpedo_num>0):
                        Sharpedo_num=Sharpedo_num-minus_num-2
                    if(Carvaha_num>0):
                        Carvaha_num=Carvaha_num-minus_num-2
                    if(Feebas_num>0):
                        Feebas_num=Feebas_num-minus_num-2
                    if(Shiny_num>0):
                        Shiny_num=Shiny_num-minus_num-2
                except:
                    print("Somthing wrong in Pokemon_name _analyze")
                    
                    
                cv2.putText(img, now_pokemon_name, [10,23], cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)  
                cv2.putText(img, "S:"+str(Sharpedo_num), [10,46], cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)  
                cv2.putText(img, "C:"+str(Carvaha_num), [10,69], cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)  
                cv2.putText(img, "F:"+str(Feebas_num), [10,92], cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2) 
                cv2.putText(img, "SH:"+str(Shiny_num), [10,115], cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 2)  
                
                
                
                cv2.imshow('battle_pokemon_detector', img)
                if cv2.waitKey(25) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()
                    break     

from multiprocessing import Process, Queue, Pipe
def print_global_variable(n):
    while(True):
        time.sleep(1)
        print(now_pokemon_name)
        
 
if __name__ == "__main__": 
    PD = Pokemmo_Detector()
    conn_send, conn_recv = Pipe() #生成管道的两边，分别传给两个进程
    PD.start_pokemmo_monitor()
    #PD.start_battle_monitor(10)
    # creating processes 
    """ p1 = multiprocessing.Process(target=PD.start_battle_monitor, args=(conn_send, )) 
    p2 = multiprocessing.Process(target=PD.start_water_monitor, args=(conn_recv, )) 
    
    p1.start()
    p2.start()
    
    p1.join() 
    p2.join()"""
   # PD.start_battle_monitor(conn_recv)
   # 
   # 
   # 


     