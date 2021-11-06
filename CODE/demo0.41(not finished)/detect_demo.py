
# _*_ coding:UTF-8 _*_
"""
pip install --upgrade setuptools
pip install numpy Matplotlib
pip install opencv-python
pip install pyautogui
pip install mss
pip install pynput"""
import pyautogui
from pynput.keyboard import Key, Controller
import cv2

import os,sys
sys.path.append(r'C:/Users/mizukiyuta/Desktop/pokemmo-mizuki/')    #要用绝对路径
#print(sys.path)        #查看模块路径
import mss
import numpy
import matplotlib.pyplot as plt
import time
import copy
N=10

player_img_list=[]
tw_list=[]
th_list=[]

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
#player_img_list,player_w_list,player_h_list=[],[],[]
Player_data_num=10
player_img_list,player_w_list,player_h_list=read_img("player",Player_data_num)


Ball_data_num=10
ball_img_list,ball_w_list,ball_h_list=read_img("ball",Ball_data_num)


Me_data_num=4
me_img_list,me_w_list,me_h_list=read_img("me",Me_data_num)
##Mizuki located at abotu（632，358） 1280/2+-10   720/2+-10
from scipy.spatial.distance import pdist, squareform
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



if __name__ == "__main__":
    #print("break1")
    run_i=0
    with mss.mss() as sct:
        # Part of the screen to capture
        #1280*720
        monitor = {'top': 60, 'left': 0, 'width': 1280, 'height': 720}
        b_point_list=[]
        while 'Screen capturing':
            run_i=run_i+1
            # Get raw pixels from the screen, save it to a Numpy array
            img = numpy.array(sct.grab(monitor))
            #img_gray=img
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            """
            res_list=[]
            for i in range(Player_data_num):
                #res = cv2.matchTemplate(img_gray, player_img_list[i], cv2.TM_CCOEFF_NORMED)
                res = cv2.matchTemplate(img_gray, player_img_list[i], cv2.TM_CCOEFF_NORMED)
                res_list.append(res)
            threshold = 0.62
            for j in range(Player_data_num):
                loc2 = numpy.where(res_list[j] >= threshold)
                for pt in zip(*loc2[::-1]):
                    cv2.rectangle(img, pt, (pt[0] + player_w_list[j], pt[1] + player_h_list[j]), (0, 0, 255), 2)
            """
            
            res_list=[]
            for i in range(Ball_data_num):
                #res = cv2.matchTemplate(img_gray, player_img_list[i], cv2.TM_CCOEFF_NORMED)
                res = cv2.matchTemplate(img_gray, ball_img_list[i], cv2.TM_CCOEFF_NORMED)
                res_list.append(res)
            threshold = 0.62
            for j in range(Ball_data_num):
                loc2 = numpy.where(res_list[j] >= threshold)
                for pt in zip(*loc2[::-1]):
                    cv2.rectangle(img, pt, (pt[0] + ball_w_list[j], pt[1] + ball_h_list[j]), (0, 255, 0), 2)
                    x = int(pt[0]+ball_w_list[j]*0.5)
                    y = int(pt[1]+ball_h_list[j]*0.5)
                    b_point_list.append([x,y])
                    cv2.rectangle(img, (x,y), (x+2,y+2), (0,0, 255), 2)
            
            #cv2.rectangle(img, (640-10,350-10), (640-10 + 20, 350+20), (0, 255, 255), 2)
            cv2.rectangle(img, (640,350-130), (640 + 2, 350-130+2), (255, 255, 255), 2)
            if(run_i>=15):
                #print(b_point_list)
                #print("###ball point###")
                #print(b_point_list)
                if(len(b_point_list)>0):
                    b_point_list = delete_same_point(b_point_list)
                else:
                    pass
                #for i in b_point_list:
                #print("###same point deleted###")
                
                
                """
                at_fish_point=False
                for p in b_point_list:
                    if(p[0]<655 and p[0]>625):
                        if(p[1]<235 and p[1]>205):
                            at_fish_point=True
                """

                b_point_list1=copy.deepcopy(b_point_list)#left-right

                b_point_list2=copy.deepcopy(b_point_list)#up_down

                
                
                b_point_list1.sort(key=lambda x:(x[0],x[1]))#x从小到大，y从小到大
                
                b_point_list2.sort(key=lambda x:(x[1],x[0]))#y从小到大，x从小到大
                
                b_point_list_left=b_point_list1[:3]
                b_point_list_right=copy.deepcopy(b_point_list1[-3:])
                b_point_list_right.sort(key=lambda x:(x[0],x[1]))
                
                
                b_point_list_up=copy.deepcopy(b_point_list2[:3])
                b_point_list_down=copy.deepcopy(b_point_list2[-3:])
                
                b_point_list_up.sort(key=lambda x:(x[0],x[1]))
                b_point_list_down.sort(key=lambda x:(x[0],x[1]))
                
                print("b_point_list:",b_point_list)
                print("b_point_list_left:",b_point_list_left)
                print("b_point_list_right:",b_point_list_right)
                print("b_point_list_up:",b_point_list_up)
                print("b_point_list_down:",b_point_list_down)
                """for i in range(len(b_point_list)):
                    b_point_list[i][0]=b_point_list[i][0]-640
                    b_point_list[i][1]=b_point_list[i][1]-220
                """    
                #print(b_point_list)
                def pattern(p_list,mark):
                    print(mark)
                    p1=p_list[0]
                    p2=p_list[1]
                    p3=p_list[2]
                    if(abs(p2[0]-p1[0])<(64+5) and abs(p2[0]-p1[0])>(64-5)):
                        if(abs(p3[0]-p2[0])<(0+5) ):
                            if(abs(p3[1]-p2[1])<(128+5) and abs(p3[1]-p2[1])>(128-5)):
                                print("pattern1左三角")
                        elif(abs(p3[0]-p2[0])<(64+5) and abs(p3[0]-p2[0])>(64-5)):
                            if((p3[1]-p2[1])<(64+5) and (p3[1]-p2[1])>(64-5)):
                                print("pattern2上三角")
                            if((p3[1]-p2[1])<(-64+5) and (p3[1]-p2[1])>(-64-5)):
                                print("pattern3下三角")
                    elif(abs(p2[0]-p1[0])<(0+5)):
                        if(abs(p2[1]-p1[1])<(128+5) and abs(p2[1]-p1[1])>(128-5)):
                            if(abs(p3[1]-p2[1])<(64+5) and abs(p3[1]-p2[1])>(64-5)):
                                if(abs(p3[1]-p1[1])<(64+5) and abs(p3[1]-p1[1])>(64-5)):
                                    print("pattern4右三角")
                    pass
                if(len(b_point_list)>=3 ):
                    pattern(b_point_list_left,"left")
                    pattern(b_point_list_right,"right")
                    pattern(b_point_list_up,"up")
                    pattern(b_point_list_down,"down")
                print("#"*30)
                run_i=0
                b_point_list=[]
                #cv2.destroyAllWindows()
                
            """
            res_list=[]
            for i in range(Me_data_num):
                #res = cv2.matchTemplate(img_gray, player_img_list[i], cv2.TM_CCOEFF_NORMED)
                res = cv2.matchTemplate(img_gray, me_img_list[i], cv2.TM_CCOEFF_NORMED)
                res_list.append(res)
            threshold = 0.78
            for j in range(Me_data_num):
                loc2 = numpy.where(res_list[j] >= threshold)
                for pt in zip(*loc2[::-1]):
                    cv2.rectangle(img, pt, (pt[0] + me_w_list[j], pt[1] + me_h_list[j]), (255, 0, 0), 2)
                    #print(pt[0]+me_w_list[j]*0.5,pt[1] + me_h_list[j])
            """
            
            cv2.imshow('OpenCV/Numpy normal', img)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break
            
            
            
            
            
            
            
            
            