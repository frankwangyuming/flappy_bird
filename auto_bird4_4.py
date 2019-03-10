#!/usr/bin/env python
# coding:utf-8




from __future__ import print_function
import sys
sys.path.append("game/")
import bird4_4 as game
import random
import numpy as np
from collections import deque
import pygame
import json
from sys import exit #引入sys中exit函数
from pygame.locals import *


GAME = 'bird' # 日志文件中游戏的名称
CONFIG = 'nothreshold'
ACTIONS = 2 # 有效动作的数量


game_state = game.GameState() 
# 执行规定动作

delta_x = 200
delta_y = 0

# 4.1 初始化离散状态，20pixes为一个格，高40格，宽15格
#states = 20*np.ones([40,15,2])
#states[:,:,1]=5
states = np.load('bird51.npy')
# i,j,a为对应的状态指数
i = int(delta_y//20 + 25)
j = int(delta_x//20)


# 4.3 list存飞行路径
fly_path = []
terminal = False
gamma = 0.95
count = 0

while True:

    
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()

    reward = 0
    
    i = int(delta_y//20 + 25)
    j = int(delta_x//20)
    
    # 4.2 飞行动作根据状态环境而定
    
    ratio = states[i,j,1]/(states[i,j,0]+states[i,j,1])
    print(ratio)
    if random.random()<ratio:
        action = 1
    else:
        action = 0

    # 4.3 用list存飞行路径fly_path
    if terminal==False:
        fly_path.append([i,j,action])

    #a_t = random.randint(0,2)
    
    image_data,reward,terminal,[delta_x,delta_y]= game_state.frame_step(action)
    
    # 4.4 根据reward和terminal状态更新fly_path内的q(s,a)
    if terminal==True or reward==1 or reward == -1:
        for iter,index in enumerate(fly_path):
            i_index = index[0]
            j_index = index[1]
            a_index = index[2]
            states[i_index,j_index,a_index] += reward * pow(gamma,(len(fly_path)-iter))
            if states[i_index,j_index,a_index]<0:
                states[i_index,j_index,a_index]=1
        fly_path=[]
        count +=1

    if count%100==99:
        name = 'bird%d.npy'%(count//100)
        np.save(name,states)
        
    #game.showScore('5')
