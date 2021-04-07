import pygame
from pygame.locals import *
from sys import exit
import random
import time
import copy
from mazesolver import bfs_mazesolver,back_maze,farest
def reverse(a):
    b=copy.deepcopy(a)
    for j in range((len(b)//2)):
        b[j],b[len(b)-1-j]=b[len(b)-1-j],b[j]
    return b

def juzhenprint(a):#打印矩阵
    for j in a:
        print(j)
def changejuzhen(juzhen,snake):#改变矩阵
    juzhen2=copy.deepcopy(juzhen)
    for j in snake:
        juzhen2[j[0]][j[1]]=0
    return juzhen2

def changelist(a):#改变列表
    b=copy.deepcopy(a)
    b[0]=b[0]//20
    b[1]=b[1]//20
    return [b[1],b[0]]
def changesnake(snake):#改变蛇的信息
    snake2=copy.deepcopy(snake)
    result=[]
    for j in snake2:
        result=result+[changelist(j)]
    #print(result)
    return result
def vectminus(a,b):
    return [a[0]-b[0],a[1]-b[1]]
def exchange(a):
    return [a[1],a[0]]
def next_judge(a,b):
    return abs(a[0]-b[0])+abs(a[1]-b[1])==1
def change(a):
    return [revers(a[1]),revers(a[0])]
def revers(ab):
    a=copy.deepcopy(ab)
    for j in range(len(a)):
        a[j]=-a[j]
    return a
pygame.init()
chushi=1#蛇身初始长度
long2=300#屏幕长
wid=300#屏幕宽
screen = pygame.display.set_mode((long2,wid))#显示屏幕
picturefood="snake\\food2.jpg"
picturebrain="snake\\brain2.jpg"
picturtail="snake\\tail.png"
picturheng="snake\\heng.png"
picturshu="snake\\shu.png"
pictur15="snake\\1.5.png"
pictur45="snake\\4.5.png"
pictur75="snake\\7.5.png"
pictur105="snake\\10.5.png"
snakebrain=pygame.image.load(picturebrain).convert()
food=pygame.image.load(picturefood).convert_alpha()
tail=pygame.image.load(picturtail).convert()
heng=pygame.image.load(picturheng).convert()
shu=pygame.image.load(picturshu).convert()
dirct15=pygame.image.load(pictur15).convert()
dirct45=pygame.image.load(pictur45).convert()
dirct75=pygame.image.load(pictur75).convert()
dirct105=pygame.image.load(pictur105).convert()

snakeposchushi=[0,0]
snakepos=copy.deepcopy(snakeposchushi)
snakebrainlong=20
speed=0.02#越小越快
x0=snakebrainlong
y0=0
#x0,y0代表运动趋势
long=chushi
posju=[[-1,-1] for j in range(long)]
foodpos=[20,20]#生成初始食物坐标
s=1
font=pygame.font.SysFont("arial",25)
juzhen=[[1 for i in range(long2//snakebrainlong)]for j in range(wid//snakebrainlong)]
vit=[]
over=0
while(1):
    text = font.render("score:%d" % (long-chushi), True, (255, 255, 255), (0, 255, 0))#分数显示
    time.sleep(speed)
    for e in pygame.event.get():
        if e.type==QUIT:
            exit()
    screen.fill((0, 255, 0))#填充绿色
    
    screen.blit(food, foodpos)#显示食物
    screen.blit(snakebrain, snakepos)#显示蛇头
    screen.blit(tail, posju[len(posju) - 1])#显示蛇尾
    
    allvalue=[snakepos]+posju
    for i in range(1,len(allvalue)-1,1):
        nextminus=[vectminus(allvalue[i-1],allvalue[i])]+[vectminus(allvalue[i],allvalue[i+1])]

        if(nextminus==[[0,20],[20,0]] or nextminus== [[-20,0],[0,-20]]):
            screen.blit(dirct75,allvalue[i])

        elif(nextminus==[[20,0],[0,20]] or nextminus== [[0,-20],[-20,0]]):
            screen.blit(dirct15,allvalue[i])

        elif(nextminus==[[20,0],[0,-20]]or nextminus==[[0,20],[-20,0]]):
            screen.blit(dirct45,allvalue[i])

        elif(nextminus==[[0,-20],[20,0]]or nextminus==[[-20,0],[0,20]]):
            screen.blit(dirct105,allvalue[i])

        elif(nextminus==[[20,0],[20,0]]or nextminus==[[-20,0],[-20,0]] or nextminus==[20,0] or nextminus==[-20,0]):
            screen.blit(heng,allvalue[i])

        elif(nextminus==[[0,20],[0,20]]or nextminus==[[0,-20],[0,-20]] or nextminus==[0,20] or nextminus==[0,-20]):
            screen.blit(shu,allvalue[i])


#speed
    #核心算法
    snakeallpos = changesnake(posju)  # 生成蛇位置信息，不包括蛇头
    #print(snakeallpos)
    cjuzhen = changejuzhen(juzhen, snakeallpos)  # 生成游戏信息矩阵，蛇身体为0(不包括蛇头)，空白和食物部分为1
    wheretogo = bfs_mazesolver(cjuzhen, changelist(snakepos), changelist(foodpos))#计算应该怎么走
    if(wheretogo!=0):#存在方案
        if(len(wheretogo)>=len(snakeallpos)+2):#方案比蛇身长
            vit=wheretogo[len(wheretogo)-(len(snakeallpos)+2):len(wheretogo)]#得到虚拟蛇吃完食物后的形态,包括蛇头蛇尾,存在bug,相对位置
            vit=reverse(vit)
        else:
            vit=reverse(wheretogo)+snakeallpos[0:len(snakeallpos)+2-len(wheretogo)]
        cjuzhen=changejuzhen(juzhen,vit[1:len(vit)-1])#判断吃到食物后能否达到蛇尾,排除两端
        if(bfs_mazesolver(cjuzhen,vit[0],vit[len(vit)-1])==0):#吃完食物后找不到蛇尾
            #print("exit ways but can't find tail after eat")
            wheretogo=0
    if(wheretogo==0 ):#不能直接到达食物或者吃完食物找不到蛇尾
        cjuzhen=changejuzhen(juzhen,snakeallpos[0:len(snakeallpos)-1])#生成游戏信息矩阵
        wheretogo=farest(cjuzhen,changelist(snakepos),snakeallpos[len(snakeallpos)-1])#以蛇尾为目标

    if(wheretogo!=0 and len(wheretogo)>=2):

        panding = exchange(vectminus(wheretogo[1], changelist(snakepos)))
        if panding == [0, -1]:  # 上
            y0 = -snakebrainlong
            x0 = 0
        elif panding == [0, 1]:  # 下
            y0 = snakebrainlong
            x0 = 0
        elif panding == [-1, 0]:  # 左
            y0 = 0
            x0 = -snakebrainlong
        elif panding == [1, 0]:  # 右
            y0 = 0
            x0 = snakebrainlong

    panbie=snakepos[0]+x0>long2-snakebrainlong or \
      snakepos[1]+y0>wid-snakebrainlong or \
      snakepos[0]+x0<0 or \
      snakepos[1]+y0<0 or \
      [snakepos[0]+x0,snakepos[1]+y0] in posju[0:len(posju)-1]#计算判定值
    if panbie:#撞到自己或者边界
        time.sleep(600)
        #print("false")
        #print(x0,y0)
        s = 0

    if(s==1):#没有撞到
        before_move=posju[len(posju)-1]
        posju = [copy.deepcopy(snakepos)] + copy.deepcopy(posju[0:len(posju) - 1])
        snakepos[0]=snakepos[0]+x0
        snakepos[1]=snakepos[1]+y0
    if foodpos==snakepos:#吃到食物
        #print("have eat")
        long=long+1
        posju=posju+[before_move]
        while (foodpos in posju + [snakepos]):  # 生成新食物
            m = posju + [snakepos]
            for j in range(len(m)):
                m[j] = changelist(m[j])
            a = changejuzhen(juzhen, m)
            #juzhenprint(a)
            if(a==[[0 for i in range(long2//20)] for j in range(long2//20)]):
                foodpos=[-100,-100]

                break
            foodpos = [random.randrange(0, long2, snakebrainlong), random.randrange(0, wid, snakebrainlong)]
    #screen.blit(text, (long2-120, 0))#显示分数
    pygame.display.update()
