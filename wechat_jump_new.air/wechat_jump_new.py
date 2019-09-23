# -*- encoding=utf8 -*-
__author__ = "tanglihong"

from airtest.core.api import *
import os
import cv2
import numpy as np
import time
import random
import math
import argparse


def jump(distance,pre):
    
    # 这个参数还需要针对屏幕分辨率进行优化
    press_time = int(distance * pre)/1000
    # 生成随机手机屏幕模拟触摸点
    # 模拟触摸点如果每次都是同一位置，成绩上传可能无法通过验证
    rand = random.randint(0, 9) * 10
    print("press time ",press_time)
    touch((rand,rand),duration=press_time)
    
def getdistance(p1,p2):
    x=p1[0]-p2[0]
    y=p1[1]-p2[1]
        #用math.sqrt（）求平方根
    len= math.sqrt((x**2)+(y**2))
    return len

def get_center(firstpath,top1,top2):
    img_rgb = cv2.imread(firstpath)
    # 边缘检测
    img_0 = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    canny_img=cv2.Canny(img_0, 30, 150)
    canny_img=np.uint8(np.absolute(canny_img))
#     img_rgb = cv2.GaussianBlur(img_rgb, (5, 5), 0)
#     canny_img = cv2.Canny(img_rgb, 1, 10)
    # H, W = canny_img.shape
    # 利用边缘检测的结果寻找物块的上沿和下沿
    # 进而计算物块的中心点
    height, width = canny_img.shape
    
#     去掉认为干扰
#     for y in range(top1[1], top2[1]):
#         for x in range(top1[0], top2[0]):
#             canny_img[y][x] = 0
    height_start=int(height/3)
    height_end=top1[1]+50 #int(height/3)*2
    crop_img = canny_img[height_start:height_end, 0:width]
    cv2.imwrite(r'D:\BaiduNetdiskDownload\wechat_jump.air\testbak.png', crop_img)

    is_first=True
    to_x=0
    to_y=0
    
    top_y=0
    left_x=0
    for h in range(height_start,height_end):
        h_arr=np.nonzero(canny_img[h])[0]
        if len(h_arr) > 0:
#             print('yy:',h,'arr:',h_arr)
            if is_first:
                # 第一个非0元素
                to_x=int(np.mean(h_arr))
                top_y=h
                is_first=False
            elif h_arr[-1] < 1050:
                if h_arr[-1] > left_x: #每一行找到非0元素的，最后一个
                    left_x=h_arr[-1]
                    to_y=h
    if (to_y-top_y) >150 :
        to_y=(top_y+100)
    cv2.circle(canny_img, top1, 5, 255, -1) #绘制落脚点
    cv2.circle(canny_img, top2, 5, 255, -1) #绘制落脚点
    cv2.circle(canny_img, (to_x,to_y), 5, 255, -1) #绘制落脚点
    cv2.imwrite(r'D:\BaiduNetdiskDownload\wechat_jump.air\testbakfff.png', canny_img)
    return to_x, to_y




sys.path.append('C:\\Program Files\\Python36\\Lib\\site-packages')
auto_setup(__file__)

# touch(Template(r"tpl1568813958590.png", record_pos=(0.124, 0.714), resolution=(1080, 1920)))

size_str=shell("wm size")
m = re.search(r'(\d+)x(\d+)', size_str)
height=m.group(2)
pre=2560/float(height)
print("pre ",pre)
    
for nn in range(500):
    # 查找跳棋的位置
    from_cen=find_all(Template(r"tpl1568530234457.png", record_pos=(-0.189, 0.061),resolution=(1080, 1920)))
    print("from_cen:",from_cen)
    
    if from_cen == None:
#         匹配是否在游戏界面
        if exists(Template(r"tpl1568813958590.png", record_pos=(0.124, 0.714), resolution=(1080, 1920))):
            print("在玩一局")
            touch(Template(r"tpl1568813958590.png", record_pos=(0.124, 0.714), resolution=(1080, 1920)))
        elif exists(Template(r"tpl1568814156651.png", record_pos=(0.001, 0.471), resolution=(1080, 1920))):
            print("开始游戏")
            touch(Template(r"tpl1568814156651.png", record_pos=(0.001, 0.471), resolution=(1080, 1920)))
        else:
            print("未知，结束")
            break
        sleep(2)

    
#   获取跳棋坐标
    top1=from_cen[0]['rectangle'][0]
    top2=from_cen[0]['rectangle'][2]
    from_x,from_y=from_cen[0]['result'][0],from_cen[0]['rectangle'][1][1]
    print("top1:",top1,"top2:",top2)
    print("From x:%s,y:%s",from_x,from_y)

    #匹配圆点
    to_pos=find_all(Template(r"tpl1568891410834.png", record_pos=(0.216, 0.053), resolution=(1080, 1920)))
    if to_pos == None:#边缘检测
        dirpath=os.path.split(os.path.realpath(__file__))[0]
        # print(dirpath)
        firstpath=os.path.join(dirpath,"first.png")
        snapshot(firstpath)

        to_x, to_y = get_center(firstpath,top1,top2)
    else:
        to_x,to_y=to_pos[0]['result'][0],to_pos[0]['rectangle'][1][1]
    #     print(pos2)
    #     pos2x,pos2y=pos2[0]['result'][0],pos1[0]['rectangle'][1][1]
    print("To x:%s,y:%s",to_x,to_y)
    distances=getdistance((from_x,from_y),(to_x,to_y))
    print("distance %s",distances)
    jump(distances,1.392)
    sleep(1)
    



    
# print(pos1[0]['result'])
# print(pos1[0]['rectangle'][1])
# posx,posy=pos1[0]['result'][0],pos1[0]['rectangle'][1][1]
# print(posx)
# print(posy)

# touch(Template(r"tpl1568530156719.png", record_pos=(0.002, 0.328), resolution=(1080, 1920)))
# swipe((500,1600), (500,600))
# swipe((0.5,0.9), vector=[0, 1])

# wait(Template(r"tpl1568530234457.png", record_pos=(-0.189, 0.061), resolution=(1080, 1920)))

