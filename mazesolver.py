import time
def kezou(x,y,juzhen):#只排除墙和边界可走的地方
    result=[]
    if ((y+1)<len(juzhen[0]) and juzhen[x][y+1]==1):
        result=result+['right']
    if ((x-1)>=0 and juzhen[x-1][y]==1):
        result=result+['up']
    if ((y-1)>=0 and juzhen[x][y-1]==1):
        result=result+['left']
    if ((x+1)<len(juzhen) and juzhen[x+1][y]==1):
        result=result+['down']
    return result

def nextpoint2(x,y,str):#根据字符串计算下一个点
    if str=='right':
        return [x,y+1]
    if str=='left':
        return [x,y-1]
    if str=='down':
        return [x+1,y]
    if str=='up':
        return [x-1,y]
def change_dict(a):#按键值降序提取字典键，输入为列表
    result=[]
    var=dict(sorted( a.items(),key = lambda x:x[1],reverse = 1))
    for j in var:
        result=result+[j]
    return result
def choose_farest(dirction_list,now,end):#选择最远的方向
    var={}
    for dirct in dirction_list:
        nextpoint=nextpoint2(now[0],now[1],dirct)
        var[dirct]=abs(nextpoint[0]-end[0])+abs(nextpoint[1]-end[1])
    return change_dict(var)
#print(choose_farest(["right","left","up","down"],[5,5],[6,6]))



def zouguo(a,value):   #判断一个点是否是之前走过的
    for i in value:
        if a in i:
            return 1
    return 0

def kezou2(x,y,juzhen,value):#防止走走过的地方可走的地方，返回根据这个条件可以走的方向
    result=kezou(x,y,juzhen)#计算这个点可以走的方向，仅排除被挡
    zouguole=[]
    for item in result:
        pos=nextpoint2(x,y,item)
        if zouguo(pos,value):
            zouguole=zouguole+[item]
    for j in zouguole:
        result.remove(j)
    return result
def kezou3(x,y,juzhen,arrived,now,end):
    final=[]
    result=kezou(x, y, juzhen)
    result=choose_farest(result,now,end)
    for direct_th in range(len(result)):
        nextpoint=nextpoint2(x,y,result[direct_th])#计算下一个点
        if nextpoint not in arrived:
            final=final+[result[direct_th]]
    return final


def back_maze(juzhen,start,end):#回溯法即深度优先法解迷宫,判断迷宫是否可解
    if(juzhen[start[0]][start[1]]==0):
        return 0
    result=[]
    value = []
    point = start
    pointvalue = [point, kezou2(point[0], point[1], juzhen,value)]  # 计算初始点可以走的位置
    value = value + [pointvalue]
    while (point != end):  # 迷宫核心算法，当没有达到终点时候执行
        #print(value)
        if value[len(value) - 1][1] != []:  # 存在方案不是空集
            # print(value)
            # print(point)
            point = nextpoint2(point[0], point[1], value[len(value) - 1][1][0])  # 计算下一个点坐标
            del value[len(value)-1][1][0]  # 删掉已经选择的方案
            pointvalue = [point, kezou2(point[0], point[1],juzhen,value)]  # 计算新的点和新的点可以走的位置
            value = value + [pointvalue]  # 记录求解过程
        elif value[len(value) - 1][1] == []:  # 已经被卡死，即这个点没有位置可以走，或者可走的位置被删完
            #print(point)
            if(point==start):#返回到第一个点，这个迷宫无解
                return 0
            del value[len(value) - 1]  # 删掉当前点的位置信息
            point = value[len(value) - 1][0]  # 返回上一个点
    for i in range(len(value)):
        result=result+[value[i][0]]
    return result
def bfs_mazesolver(juzhen,start,end):
    # 广度优先法解迷宫，返回最短解法路径或者解不存在提示
    if(juzhen[start[0]][start[1]]!=1):#当起点不是过道时候迷宫无解
        return 0
    if(juzhen[end[0]][end[1]]!=1):#当终点不是过道时候迷宫无解
        return 0
    if(start==end):#当起点就是终点
        return 1
    value = [[start]]
    newvalue = []
    arived = [start]
    while (1):
        for j in value:  # 遍历所有现有的走法路径
            nn = []
            newpoint = []
            lastpos = j[len(j) - 1]  # 取该方案最后一个点
            wheretogo = kezou(lastpos[0], lastpos[1], juzhen)  # 计算可以走的方案
            for way in wheretogo:
                sss = nextpoint2(lastpos[0], lastpos[1], way)  # 计算该路径此方案新到达的点
                if (sss == end):  # 如果达到终点，修改标志位。退出并返回结果
                    result = j + [end]
                    return result
                newpoint = newpoint + [sss]  # 存储新的点，注意换路径时应当清空

            for ii in newpoint:
                if ii not in arived:
                    nn=nn+[ii]

            if nn==[]:  # 如果没有达到新的点
                continue  # 跳过该路径(代表该路径是失败路径)，遍历下一个方案
            elif nn != []:  # 存在新方案
                arived = arived +nn
                for newpos in nn:
                    newvalue=newvalue+[j + [newpos]]  # 存储新的走法路径
        value = newvalue  # 赋值新的路径方案
        if(value==[]):
            return 0
        newvalue = []
def farest(juzhen,start,end):#回溯法即深度优先法解迷宫,判断迷宫是否可解
    if(juzhen[start[0]][start[1]]!=1):#当起点不是过道时候迷宫无解
        return 0
    if(juzhen[end[0]][end[1]]!=1):#当终点不是过道时候迷宫无解
        return 0
    arrived=[start]
    result=[]
    value = []
    point = start
    pointvalue = [point, kezou3(point[0], point[1], juzhen,arrived,point,end)]  # 计算初始点可以走的位置
    value = value + [pointvalue]
    while (point != end):  # 迷宫核心算法，当没有达到终点时候执行
        #print(value)
        if value[len(value) - 1][1] != []:  # 存在方案不是空集
            arrived=arrived+[point]
            #print(value)
            point = nextpoint2(point[0], point[1], value[len(value) - 1][1][0])  # 计算下一个点坐标
            del value[len(value) - 1][1][0]  # 删掉已经选择的方案
            pointvalue = [point, kezou3(point[0], point[1], juzhen,arrived,point,end)]  # 计算新的点和新的点可以走的位置
            value = value + [pointvalue]  # 记录求解过程
        elif value[len(value) - 1][1] == []:  # 已经被卡死，即这个点没有位置可以走，或者可走的位置被删完
            #print(point)
            if(point==start):#返回到第一个点，这个迷宫无解
                return 0
            del value[len(value) - 1]  # 删掉当前点的位置信息
            point = value[len(value) - 1][0]  # 返回上一个点
    for i in range(len(value)):
        result=result+[value[i][0]]
    return result
