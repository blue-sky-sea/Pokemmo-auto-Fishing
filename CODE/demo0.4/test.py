# -*- coding: utf-8 -*-
"""
Created on Thu Oct 21 21:49:47 2021

@author: mizukiyuta
"""

p=[[240,350],[240,360],[310,420],[310,420],[310,420],[390,340],[380,350],[106,88]]

xl=[]
    
#print(set(str_p))
from scipy.spatial.distance import pdist, squareform

def delete_same_point(point_list):
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
            if(dis[d]<15 and d!=i):
                need_to_delete_i.append(d)
                
    #print(need_to_delete_i) 
    new_point_list=[]
    for i in range(len(point_list)):
        if(i not in need_to_delete_i):
            new_point_list.append(point_list[i])
    return new_point_list

new_p = delete_same_point(p)    
print(new_p)

r=squareform(pdist(new_p))
print(r)

near_i_list=[]
def get_near_i(r):
    for i in range(len(r)):
        dis=r[i]
        near_i=[]
        for d in range(len(dis)):
            if(dis[d]<=160 and dis[d]>=10):
                near_i.append(d)
        near_i_list.append(near_i)
    return near_i_list
l=get_near_i(r)
print(l)

'''
for i in range(len(r)):
    dis=r[i]
    for d in range(len(dis)):
        if(dis[d]<=160 and dis[d]>=10):
            print("和",new_p[i],i,"临近",dis[d],d)'''
        
'''
temp_x=[]
new_p=[]
for i in range(len(p)-1, -1, -1):
    x=p[i][0]
    y=p[i][1]
    if(i>1):
        x2=p[i-1][0]
        y2=p[i-1][1]
        
        if(abs(x-x2)<15 and abs(y-y2)<15):
            #same point
            p.pop(i)
    print(x,y)'''