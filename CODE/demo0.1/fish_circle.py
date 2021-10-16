#
# _*_ coding:UTF-8 _*_
import win32api
import win32con
import win32gui
from ctypes import *
import ctypes
import time
from playsound import playsound
 
import random
 
from random import choice

MapVirtualKey = ctypes.windll.user32.MapVirtualKeyA
VK_CODE = {
    'backspace':0x08,
    'tab':0x09,
    'clear':0x0C,
    'enter':0x0D,
    'shift':0x10,
    'ctrl':0x11,
    'alt':0x12,
    'pause':0x13,
    'caps_lock':0x14,
    'esc':0x1B,
    'spacebar':0x20,
    'page_up':0x21,
    'page_down':0x22,
    'end':0x23,
    'home':0x24,
    'left_arrow':0x25,
    'up_arrow':0x26,
    'right_arrow':0x27,
    'down_arrow':0x28,
    'select':0x29,
    'print':0x2A,
    'execute':0x2B,
    'print_screen':0x2C,
    'ins':0x2D,
    'del':0x2E,
    'help':0x2F,
    '0':0x30,
    '1':0x31,
    '2':0x32,
    '3':0x33,
    '4':0x34,
    '5':0x35,
    '6':0x36,
    '7':0x37,
    '8':0x38,
    '9':0x39,
    'a':0x41,
    'b':0x42,
    'c':0x43,
    'd':0x44,
    'e':0x45,
    'f':0x46,
    'g':0x47,
    'h':0x48,
    'i':0x49,
    'j':0x4A,
    'k':0x4B,
    'l':0x4C,
    'm':0x4D,
    'n':0x4E,
    'o':0x4F,
    'p':0x50,
    'q':0x51,
    'r':0x52,
    's':0x53,
    't':0x54,
    'u':0x55,
    'v':0x56,
    'w':0x57,
    'x':0x58,
    'y':0x59,
    'z':0x5A,
    'numpad_0':0x60,
    'numpad_1':0x61,
    'numpad_2':0x62,
    'numpad_3':0x63,
    'numpad_4':0x64,
    'numpad_5':0x65,
    'numpad_6':0x66,
    'numpad_7':0x67,
    'numpad_8':0x68,
    'numpad_9':0x69,
    'multiply_key':0x6A,
    'add_key':0x6B,
    'separator_key':0x6C,
    'subtract_key':0x6D,
    'decimal_key':0x6E,
    'divide_key':0x6F,
    'F1':0x70,
    'F2':0x71,
    'F3':0x72,
    'F4':0x73,
    'F5':0x74,
    'F6':0x75,
    'F7':0x76,
    'F8':0x77,
    'F9':0x78,
    'F10':0x79,
    'F11':0x7A,
    'F12':0x7B,
    'F13':0x7C,
    'F14':0x7D,
    'F15':0x7E,
    'F16':0x7F,
    'F17':0x80,
    'F18':0x81,
    'F19':0x82,
    'F20':0x83,
    'F21':0x84,
    'F22':0x85,
    'F23':0x86,
    'F24':0x87,
    'num_lock':0x90,
    'scroll_lock':0x91,
    'left_shift':0xA0,
    'right_shift ':0xA1,
    'left_control':0xA2,
    'right_control':0xA3,
    'left_menu':0xA4,
    'right_menu':0xA5,
    'browser_back':0xA6,
    'browser_forward':0xA7,
    'browser_refresh':0xA8,
    'browser_stop':0xA9,
    'browser_search':0xAA,
    'browser_favorites':0xAB,
    'browser_start_and_home':0xAC,
    'volume_mute':0xAD,
    'volume_Down':0xAE,
    'volume_up':0xAF,
    'next_track':0xB0,
    'previous_track':0xB1,
    'stop_media':0xB2,
    'play/pause_media':0xB3,
    'start_mail':0xB4,
    'select_media':0xB5,
    'start_application_1':0xB6,
    'start_application_2':0xB7,
    'attn_key':0xF6,
    'crsel_key':0xF7,
    'exsel_key':0xF8,
    'play_key':0xFA,
    'zoom_key':0xFB,
    'clear_key':0xFE,
    '+':0xBB,
    ',':0xBC,
    '-':0xBD,
    '.':0xBE,
    '/':0xBF,
    '`':0xC0,
    ';':0xBA,
    '[':0xDB,
    '\\':0xDC,
    ']':0xDD,
    "'":0xDE,
    '`':0xC0}
class POINT(Structure):
    _fields_ = [("x", c_ulong),("y", c_ulong)]
def get_mouse_point():
    po = POINT()
    windll.user32.GetCursorPos(byref(po))
    return int(po.x), int(po.y)
def mouse_click(x=None,y=None):
    if not x is None and not y is None:
        mouse_move(x,y)
        time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
def mouse_dclick(x=None,y=None):
    if not x is None and not y is None:
        mouse_move(x,y)
        time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
def mouse_move(x,y):
    windll.user32.SetCursorPos(x, y)
def key_input(str='',v_code=0):
    for c in str:
        win32api.keybd_event(VK_CODE[c],MapVirtualKey(VK_CODE[c],0),0,0)
        time.sleep(0.1)
        win32api.keybd_event(VK_CODE[c],MapVirtualKey(VK_CODE[c],0),win32con.KEYEVENTF_KEYUP,0)
        time.sleep(0.1)
        
        
        
from aip import AipOcr        
APP_ID = '15899380'
API_KEY = '1QKo2wth8n6iUNBXmTIwA8rr'
SECRET_KEY = 'Ax9SNpQdAqq7XR52PELiNI88i8M92UpC'
client = AipOcr(APP_ID, API_KEY, SECRET_KEY) 
     
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()
    
from ctypes import windll
from PIL import Image
import cv2
import numpy
import pytesseract
import difflib
#判断相似度的方法，用到了difflib库
def get_equal_rate_1(str1, str2):
   return difflib.SequenceMatcher(None, str1, str2).quick_ratio()
def start_fish():
    mouse_click(580,1080)#i 580-590 1080
    time.sleep(6)
    mouse_click(560,1160)#j 560-570 1160
    time.sleep(6)
def general_ocr(filepath):
    image = get_file_content(filepath)
    results=client.general(image);
    return results



#print(results)
def cal_text_score1(text):
    feebas="Feebas"
    carva="Carvanha"
    tenta="Tentacool"
    sharpe="Sharpedo"
    feebas_score = get_equal_rate_1(feebas, text)
    carva_score = get_equal_rate_1(carva, text)
    tenta_score = get_equal_rate_1(tenta, text)
    sharpe_score = get_equal_rate_1(sharpe, text)
    scores={"Feebas":0,"Carva":0,"Tenta":0,"Sharpe":0}
    scores["Feebas"]=feebas_score
    scores["Carva"]=carva_score
    scores["Tenta"]=tenta_score
    scores["Sharpe"]=sharpe_score
    """print("feebas:",feebas_score)
    print("carva:",carva_score)
    print("tenta:",tenta_score)
    print("sharpe:",sharpe_score)"""
    print(scores)
    max_scores = max(zip(scores.values(), scores.keys()))
    print(max_scores) # (450.1, 'B')
    return max_scores,scores
def cal_text_score2(text):
    not_nibble="Not even a nibble..."
    land_pokemon="Landed a Pokémon!"
    not_nibble_score = get_equal_rate_1(not_nibble, text)
    land_pokemon_score = get_equal_rate_1(land_pokemon, text)
    print("##not_nibble_score:",not_nibble_score)
    print("##land_pokemon_score:",land_pokemon_score)
    if(not_nibble_score>land_pokemon_score and not_nibble_score>0.5):
        return 1
    elif(not_nibble_score<land_pokemon_score and land_pokemon_score>0.5):
        return 2
    elif(not_nibble_score==0 and land_pokemon_score==0):
        return 0
    elif(not_nibble_score<0.5 and land_pokemon_score<0.5):
        return 0
    else:
        return 2
def Judge_now_mode():
    # 参数说明
    # 第一个参数 开始截图的x坐标
    # 第二个参数 开始截图的y坐标
    # 第三个参数 结束截图的x坐标
    # 第四个参数 结束截图的y坐标
    bbox = (230,172,400,192)#pokemon name
    cbox = (350,82,660,132)#conversation area
    im1 = imag_grab(bbox)
    im1 = im1.convert('L')
    im1 = imag_process(im1)
    im2 = imag_grab(cbox)
    im2 = im2.convert('L')
    im1.save('name.png')
    im2.save('conver.png')

    name_text=pytesseract.image_to_string(Image.open("name.png"))
    name_text = name_text.replace(' ', '').replace('\n','').replace('\t','')
    conver_text=pytesseract.image_to_string(Image.open("conver.png"))
    conver_text = conver_text.replace('\n','').replace('\t','')
    print("##name_text is:",name_text,"***")
    print("##conver_text is:",conver_text,"***")

    max_scores,scores = cal_text_score1(name_text)
    conversation_type = cal_text_score2(conver_text)
    #print(type(scores))
    if(max_scores[0]==0):
        #没有进入战斗
        if(conversation_type==1):
            return 1,None#Not even a nibble...
        if(conversation_type==2):
            return 2,None#Landed a Pokémon!
        if(conversation_type==0):
            return 3,None#on water
        if(conversation_type==3):
            return 7,None
        else:
            return 404,None
    else:
        #可能进入战斗，也可能识别到了用户的名称
        if(conversation_type==1):
            return 4,None#Not even a nibble...
        if(conversation_type==2):
            return 5,None#Landed a Pokémon!
        if(conversation_type==0):
            return 6,max_scores#on battle
        if(conversation_type==3):
            return 7,None
        else:
            return 404,None
        
def judge_shiny():
    sbox = (230,172,400,192)#pokemon name info
    sbox2 = (560,180,900,420)#pokemon image
    im = imag_grab(sbox)
    im = im.convert('L')
    im = imag_process(im)
    #im2 = imag_grab(sbox2)
    name_text=pytesseract.image_to_string(im)
    #im2.show()
    print("JUDGE_SHINY",name_text)
    if("shiny" in name_text or 
       "hin" in name_text or 
       "iny" in name_text or 
       "ny" in name_text or
       "Shi" in name_text):
        print("!"*50)
        print("!!Shiny Pokemon!!!")
        print("!"*50)
        return True
    return False

def imag_grab(box):
    im = ImageGrab.grab(box)
    return im
def imag_process(im):
    threshold = 215
    #threshold2 = 245
    def my_thresold(threshold):
        table = []
        for i in range(256):
            if i < threshold:
                table.append(1)
            else:
                table.append(0)
        return table
    table1 = my_thresold(threshold)   
    im = im.point(table1,'1')
    # 参数 保存截图文件的路径
    #im.save('zy.png')
    return im
from PIL import ImageGrab
def find_fishpoint():
    #up 0 #down 1 #left 2 right 3
    step=0
    n=0
    m=0
    while(True):
        step=step+1
        key_input(str='i',v_code=24)
        a=random.randrange(-6,5)*0.1
        time.sleep(5+a)
        
        key_input(str='j',v_code=17)
        a=random.randrange(-2,6)*0.1
        time.sleep(6.2+a)
        
        mode,max_scores = Judge_now_mode()
        print("##",mode," possible pokemon:",max_scores)
        a=random.randrange(-3,8)*0.1
        
        if(max_scores!=None):
            print(max_scores[1])
            if(max_scores[1]=="Feebas"):
                print(max_scores[0])
                song = pygame.mixer.Sound("M09.ogg")
                song.play()
                time.sleep(1000)
            elif(max_scores[1]=="Carva"):
                print("lalalalala",max_scores[0])
        time.sleep(2.5+a)
        
        if(mode==6):
            is_shiny = judge_shiny()
            if(is_shiny==True):
                song = pygame.mixer.Sound("M09.ogg")
                song.play()
                time.sleep(1000)
            else:
                n=n+1
                mouse_click(360,405)
                print("click mouse 360,405")
                a=random.randrange(-3,5)*0.1
                time.sleep(4+a)
        elif(mode==3):
            print("mode=3 n=",n)
            time.sleep(1.2)
            if(n>=2):
                foo = ['w', 'd', 'a', 's']
                key_code = choice(foo[:2])
                key_input(str=key_code,v_code=211)
                m=m+1
                print("#"*30,"press",key_code,"to go")
                n=0
                a=random.randrange(-3,5)*0.1
                time.sleep(4+a)

        else:
            mouse_click(360,405)
            a=random.randrange(-3,5)*0.1
            time.sleep(4+a)
def fish_circle():
    while(True):
        #press I to fish，after 6s,press J
        #start_fish() 
        #mouse_click(580,1080)#i 580-590 1080
        key_input(str='i',v_code=24)
        print("#"*30)
        print("press i，模拟按键i开始钓鱼")
        a=random.randrange(-6,5)*0.1
        time.sleep(5.2+a)
        #mouse_click(560,1160)#j 560-570 1160
        key_input(str='j',v_code=17)
        print("#"*30)
        print("press j，模拟按键j确定")
        a=random.randrange(-2,6)*0.1
        time.sleep(5.5+a)
        #Judge whera go into battle mode 
        #or Not even a nibble... 
        mode,max_scores = Judge_now_mode()
        print("##",mode," possible pokemon:",max_scores)
        a=random.randrange(-3,8)*0.1
        time.sleep(3.2+a)
        if(mode==6):
            #Judge it's shiny or not
            is_shiny = judge_shiny()
            if(is_shiny==True):
                song = pygame.mixer.Sound("M09.ogg")
                song.play()
                time.sleep(1000)
            else:
                #RUN
                a=random.randrange(-6,4)*0.1
                time.sleep(1+a)
                print("#"*30)
                print("RUN，跑吧没有闪光")
                i=random.randrange(-12,10)
                j=random.randrange(-6,6)
                
                print("#"*30)
                print("click ",360+i,",",408+j)
                mouse_click(360+i,408+j)
                a=random.randrange(-3,5)*0.1
                time.sleep(4+a)

#start
#wait 5s for click to game
#press I to start fish session
#after 6s press J to confirm conversation
#Judge whera get into battle mode or fish not success,
#if fish not sucess,press I to start fish session again
#if into battle mode,judge its shine or not
if __name__ == "__main__":  
    import pygame
    pygame.init()
    """import win32guij
    handle = win32gui.FindWindow(0, "PokeMMO")
    if not handle:
        print("cannot find Pokemmo window")
    else:
        print(handle)
    """
    print("#"*30)
    print("Start fishing,please click to Pokemmo's window")
    time.sleep(4)
    print("...Start fishing!")  
    print("#"*30)
    print()
          
    fish_circle() 
    #find_fishpoint()
                
            
        
    
    
    
    
    
    
    #time.sleep(8)
    #mouse_click(600,1160)#k 590-610 1160