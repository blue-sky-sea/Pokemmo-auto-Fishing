# -*- coding: utf-8 -*-
"""
Created on Sun Oct 24 16:24:54 2021

@author: mizukiyuta
"""

#IMPORT LIB
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
import random
import multiprocessing 

#read_img_data
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
feebas_img_list,feebas_w_list,feebas_h_list=[],[],[]
Feebas_data_num=9
feebas_img_list,feebas_w_list,feebas_h_list=read_img("feebas",Feebas_data_num)

group_img_list,group_w_list,group_h_list=[],[],[]
Group_data_num=5
group_img_list,group_w_list,group_h_list=read_img("group",Group_data_num)

player_img_list,player_w_list,player_h_list=[],[],[]
Player_data_num=8
player_img_list,player_w_list,player_h_list=read_img("player",Player_data_num)

shiny_img_list,shiny_w_list,shiny_h_list=[],[],[]
Shiny_data_num=1
shiny_img_list,shiny_w_list,shiny_h_list=read_img("shiny",Shiny_data_num)



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
def getNextMove(goalx,goaly,player_orientation):
	x=goalx
	y=goaly
	position="Other"
	next_move=["Stop"]
	print("(370-x):",(370-x),"  (345-y):",(345-y))
	#在同一列上，x之间的差距不超过20
	if(abs(370-x)<=20):
		if((345-y)>100 and (345-y)<145):
			print((345-y),"On Fishing pot Down",(370-x))
			position="Down"
			if(player_orientation!="Up"):
				next_move=["Up","Fish"]
			else:
				next_move=["Fish"]
		elif((345-y)<-50):
			next_move=["Down","Fish"]
		elif((345-y)>155):
			next_move=["Up","Fish"]
		elif((345-y)<25 and (345-y)>-25):
			print((345-y),"On Fishing pot Up",(370-x))
			position="Up"
			if(player_orientation!="Down"):
				next_move=["Down","Fish"]
			else:
				next_move=["Fish"]
	#在左边同一列上
	elif((370-x)<-50 and (370-x)>-80):
		#print("On left")
		if((345-y)<70 and (345-y)>40):
			print((345-y),"On Fishing pot Left",(370-x))
			position="Left"
			if(player_orientation!="Right"):
				next_move=["Right","Fish"]
			else:
				next_move=["Fish"]
		elif(((345-y))>100):
			next_move=["Right","Fish"]
		elif((345-y)<30 and (345-y)>-30):
			next_move=["Right","Fish"]
		elif((345-y)<-50):
			next_move=["Down","Fish"]

	#在右边同一列上     
	elif((370-x)>50 and (370-x)<80):
		#print("On Right")
		if((345-y)<70 and (345-y)>40):
			print((345-y),"On Fishing pot Right",(370-x))
			position="Right"
			if(player_orientation!="Left"):
				next_move=["Left","Fish"]
			else:
				next_move=["Fish"]
		elif(((345-y))>100):
			next_move=["Left","Fish"]
		elif((345-y)<30 and (345-y)>-30):
			next_move=["Left","Fish"]
		elif((345-y)<-50):
			next_move=["Down","Fish",""]
		pass
	#在左边较远处
	elif((370-x)<-100):
		next_move=["Right"]
	#在右边较远处
	elif(((370-x)>100)):
		next_move=["Left"]
	#在上边较远处
	elif((345-y)<-100):
		next_move=["Down"]
	elif((345-y)>100):
		next_move=["Up"]
	return next_move,position

#return group_points,player_points
def Detect_Group_Player():
	monitor = {'top': 50, 'left': 260, 'width': 780, 'height': 560}
	MAX_I=15
	capture_i=0
	total_group_points=[]
	total_player_points=[]
	with mss.mss() as sct:
		while 'Screen capturing':
			capture_i=capture_i+1
			img = numpy.array(sct.grab(monitor))  
			img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

			#匹配Group和Player
			#----------------------------------------------------------------------------
			#Group return group_points
			group_res_list=[]
			for i in range(Group_data_num):
				#res = cv2.matchTemplate(img_gray, player_img_list[i], cv2.TM_CCOEFF_NORMED)
				res = cv2.matchTemplate(img_gray, group_img_list[i], cv2.TM_CCOEFF_NORMED)
				group_res_list.append(res)
			group_points=[]
			threshold = 0.82
			for j in range(Group_data_num):
				loc2 = numpy.where(group_res_list[j] >= threshold)
				for pt in zip(*loc2[::-1]):
					cv2.rectangle(img, pt, (pt[0] + group_w_list[j], pt[1] + group_h_list[j]), (255, 0, 0), 2)
					center_x = round((pt[0]+0.5*group_w_list[j])/10)*10
					center_y = round((pt[1]+0.5*group_h_list[j])/10)*10
					group_points.append([center_x,center_y])
			#group_points=[]    
			if(len(group_points)>0):
				group_points = delete_same_point(group_points,15)
				total_group_points=total_group_points+group_points
			#----------------------------------------------------------------------------
			#Player return player_points
			player_res_list=[]
			for i in range(Player_data_num):
				res = cv2.matchTemplate(img_gray, player_img_list[i], cv2.TM_CCOEFF_NORMED)
				player_res_list.append(res)
			player_points=[]
			threshold = 0.64
			for j in range(Player_data_num):
				loc2 = numpy.where(player_res_list[j] >= threshold)
			for pt in zip(*loc2[::-1]):
				cv2.rectangle(img, pt, (pt[0] + player_w_list[j], pt[1] + player_h_list[j]), (0, 0, 255), 2)
				center_x = round((pt[0]+0.5*player_w_list[j])/10)*10
				center_y = round((pt[1]+0.5*player_h_list[j])/10)*10
				player_points.append([center_x,center_y])
			#删除 player_points中实际上就是同一个点的数据
			#player_points=[]
			if(len(player_points)>0):
				player_points = delete_same_point(player_points,15)
				total_player_points=total_player_points+player_points
			#----------------------------------------------------------------------------
			
			cv2.imshow("test", img)
			#print("total_group_points:",total_group_points)
			#print("total_player_points",total_player_points)
			#print(capture_i,MAX_I)
			if cv2.waitKey(15) & 0xFF == ord('q'):
				cv2.destroyAllWindows()
			if(capture_i>=MAX_I):
				cv2.destroyAllWindows()
				#print("total_group_points:",total_group_points)
				#print("total_player_points",total_player_points)
				if(len(total_group_points)>0):
					total_group_points = delete_same_point(total_group_points,15)
				if(len(total_player_points)>0):
					total_player_points = delete_same_point(total_player_points,15)
				return total_group_points,total_player_points

def Detect_Battle_Pokemon():
	monitor = {'top': 50, 'left': 260, 'width': 780, 'height': 560}
	MAX_I=15
	capture_i=0
	total_feebas_points=[]
	total_shiny_points=[]
	feebas_num=0
	shiny_num=0
	have_Shiny,have_Feebas=False,False
	with mss.mss() as sct:
		while 'Screen capturing':
			capture_i=capture_i+1
			img = numpy.array(sct.grab(monitor))  
			img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

			#----------------------------------------------------------------------------
			#Feebas return Feebas_points
			feebas_res_list=[]
			for i in range(Feebas_data_num):
				res = cv2.matchTemplate(img_gray, feebas_img_list[i], cv2.TM_CCOEFF_NORMED)
				feebas_res_list.append(res)
			threshold = 0.6
			for j in range(Feebas_data_num):
				loc2 = numpy.where(feebas_res_list[j] >= threshold)
				for pt in zip(*loc2[::-1]):
					feebas_num=feebas_num+1

			#----------------------------------------------------------------------------
			#Shiny 
			shiny_res_list=[]
			for i in range(Shiny_data_num):
				res = cv2.matchTemplate(img_gray, shiny_img_list[i], cv2.TM_CCOEFF_NORMED)
				shiny_res_list.append(res)
			threshold = 0.6
			for j in range(Shiny_data_num):
				loc2 = numpy.where(shiny_res_list[j] >= threshold)
				for pt in zip(*loc2[::-1]):
					shiny_num=shiny_num+1

			if(capture_i>=MAX_I):
				if(feebas_num>=1):
					have_Feebas=True
				if(shiny_num>=1):
					have_Shiny=True
			
				return have_Shiny,have_Feebas
#
def Players_Mode(group_points,player_points):
	#判断有钓鱼麻将桌，还是在分散找鱼点
	have_group,have_player,is_player_seperate=False,False,False
	if(len(group_points)>=1):
		have_group=True
	if(len(player_points)>=2 and len(player_points)<=7):
		have_player=True
		#my_point=[370,345]
		g_point=[370,355]
		if(len(group_points)!=0):
			g_point=group_points[0]

		seperate_num=0
		for p_point in player_points:
			x_= abs(g_point[0]-p_point[0]) 
			y_= abs(g_point[1]-p_point[1]) 
			if(y_>155 or x_>80):
				seperate_num=seperate_num+1
		if(seperate_num>len(player_points)*0.6):
			is_player_seperate=True
	elif(len(player_points)>7):
		have_player=True
		is_player_seperate=True
	return have_group,have_player,is_player_seperate

def get_average_position(points):
	total_x=0
	total_y=0
	for i in range(len(points)):
		if(points[i][0]>=365 and points[i][0]<=385):
			if(points[i][1]>=345 and points[i][1]<=370):
				continue
		total_x = total_x+points[i][0]
		total_y = total_y+points[i][1]
	average_x=int(total_x/len(points))
	average_y=int(total_y/len(points))
	return average_x,average_y

def delete_myself_point(points):
	new_points=[]
	for i in range(len(points)):
		if(points[i][0]>=365 and points[i][0]<=385):
			if(points[i][1]>=345 and points[i][1]<=370):
				continue
		new_points.append(points[i])
	return new_points

def Move_or_Fish(player_orientation):
	move_or_fish="MOVE"
	group_points,player_points=Detect_Group_Player()
	group_points=delete_myself_point(group_points)
	print("group_points,player_points:",group_points,player_points)
	have_group,have_player,is_player_seperate = Players_Mode(group_points,player_points)
	print("have_group,have_player,is_player_seperate:",have_group,have_player,is_player_seperate)
	#何时该移动？
	#存在钓鱼麻将桌，离玩家较远
	#已经到达钓点，玩家方向不朝着鱼点
	#玩家很分散，大家都在找鱼点
	goalx=370
	goaly=345
	next_move=["Stop"]
	position="Other"
	if(have_group==True):
		if(have_player==True):
			goalx,goaly=get_average_position(player_points)
		if(have_player==False):
			goalx=group_points[0][0]
			goaly=group_points[0][1]
		next_move,position=getNextMove(goalx,goaly,player_orientation)
		#向着group移动
	else:
		if(have_player==True):
			goalx,goaly=get_average_position(player_points)
			next_move,position=getNextMove(goalx,goaly,player_orientation)
			
		else:
			next_move=[player_orientation,"Fish"]
			position="Other"
			#向着当前玩家朝向前进
	#何时该钓鱼？
	#已经到达钓点，并且玩家方向朝着鱼点
	#玩家很分散，大家都在找鱼点
	pass
	if(position=="Other"):
		move_or_fish="MOVE"
	else:
		move_or_fish="FISH"
	return move_or_fish,next_move

def Feebas_Shiny_or_Run():
	have_Shiny,have_Feebas=False,False

	have_Shiny1,have_Feebas1 = Detect_Battle_Pokemon()
	have_Shiny2 = Brain_controller.Judge_shiny()
	have_Feebas2,is_shiny = Brain_controller.Judge_Feebas()
	print("[Feebas_Shiny_or_Run()] Shiny",have_Shiny1,have_Shiny2)
	print("[Feebas_Shiny_or_Run()] Feebas",have_Feebas1,have_Feebas2)
	if(have_Shiny1==True or have_Shiny2==True):
		have_Shiny=True
	if(have_Feebas1==True and have_Feebas2==True):
		have_Shiny=True

	return have_Feebas,have_Shiny

def getMoveCode(move_name):
	move_dic={"Left":"a","Right":"d","Up":"w","Down":"s","Stop":"","":"","Fish":"i"}
	random_mov_dic=["w","s","a","d"]
	if(move_name=="Random"):
		return random.choice(random_mov_dic)
	return move_dic[move_name]
def getMoveName(move_code):
	move_name_dic={"a":"Left","d":"Right","w":"Up","s":"Down","":"","i":"Fish"}
	return move_name_dic[move_code]

def do_player_action(next_move,player_orientation):
	now_orientation=player_orientation
	for move in next_move:
		move_code = getMoveCode(move)
		Move_controller.key_input(str=move_code)
		if(move=="Left" or move=="Right" or move=="Up" or move=="Down"):
			now_orientation = getMoveName(move_code)
		else:
			pass
		#print("[press]",move_code,move," [now_orientation]",now_orientation)
		Move_controller.key_input(str="j")
		time.sleep(1)
	return now_orientation
def main():
	time.sleep(4)
	Move_controller.key_input(str="w")
	player_orientation="Up"
	while(True):
		scene = Brain_controller.Judge_scene()
		if(scene=="water"):
			#如果在水面上，判断该移动还是该钓鱼
			print()
			print("[ONWATER]")
			move_or_fish,next_move = Move_or_Fish(player_orientation)
			print("move_or_fish,next_move",move_or_fish,next_move)
			if(move_or_fish=="MOVE"):
				player_orientation = do_player_action(next_move,player_orientation)
			if(move_or_fish=="FISH"):
				player_orientation = do_player_action(next_move,player_orientation)
			pass
		if(scene=="battle"):
			print()
			print("[Battle]")
			have_Feebas,have_Shiny = Feebas_Shiny_or_Run()
			#如果在战斗中，判断该逃跑，还是出现了闪光
			if(have_Shiny==True):
				import pygame
				pygame.init()
				song = pygame.mixer.Sound("M09.ogg")
				song.play()
				time.sleep(1000)
			elif(have_Shiny==False):
				Move_controller.key_input(str="sd")
				time.sleep(1)
				Move_controller.key_input(str="j")
				time.sleep(5)

			pass

if __name__ == "__main__": 
    main()
