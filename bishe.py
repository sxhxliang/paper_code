# coding:utf-8

import numpy as np
import matplotlib.pyplot as plt
import os
#读取csv文件
import csv

from seat_a_star import getAllSeatDis


count = 0
max_count = 100

# EXIT_X = [16420,34720,6565,43875]
# EXIT_Y = [30852,6587,18720,18720]

TOP_EXIT = (16.420,30.852)
BOTTOM_EXIT = (34.720,6.587)
LEFT_EXIT = (6.565,18.720)
RIGHT_EXIT = (43.875,18.720)


#座位的坐标
label = []
x = []
y = []
samply_left, samply_right = 300, 600
pre_room_len, pre_room_width = 20, 10

#存储每个人到上下左右通道的距离
top_door_distance_set = []
bottom_door_distance_set = []
left_door_distance_set = []
right_door_distance_set = []

#用于存最后座位分区的坐标
select_top_x = []
select_top_y = []
select_bottom_x = []
select_bottom_y = []
select_left_x = []
select_left_y = []
select_right_x = []
select_right_y = []
people_select = []

# 选择出口行人和门的距离
select_left_dis = []
select_right_dis = []


# 座位坐标字典
# {1:[x,y]}
dict_point = {}
# 座位和出口距离字典
# {i:[top_door_distance,bottom_door_distance,left_door_distance,right_door_distance]}
dict_dis = {} 
# 选择门的字典,用于计算人数
# {i:[top_door_distance,bottom_door_distance,left_door_distance,right_door_distance]}
dict_select_door_top = {}
dict_select_door_bottom = {}
dict_select_door_left = {}
dict_select_door_right = {}

# # 用于时间排序
array_select_door_top_time = {}
array_select_door_bottom_time = {}
array_select_door_left_time = {}
array_select_door_right_time = {}


finished_time = []

#用于标记左右两门完全疏散时间
# exit_left_time = 0
# exit_right_time =0


Velocity = 1  # m/s
Num = []
WidthDoor = 0.5
#TODO 门宽
TOPWIDTHDOOR = 0.5
TOPWIDTHDOOR = 0.5
TOPWIDTHDOOR = 0.5
TOPWIDTHDOOR = 0.5
CPeople = 1.33  # m/s


#清洗数据
def fiterPoint(px,py):
    p_x,p_y =[],[]
    for i in px:
        if i != None:
            # print(i)
            p_x.append(i)
    for i in py:
        if i != None:
            p_y.append(i)
    return p_x,p_y


def calDoorDistance(x1, y1, x2, y2):
    x1 = float(x1)
    y1 = float(y1)
    x2 = float(x2)
    y2 = float(y2)
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


def distance(people_x, people_y, door_point):
    dis_set = []
    lenght = len(people_x)
    # print(lenght)
    for item in range(lenght):
        # print(item)
        dis = calDoorDistance(people_x[item], people_y[item], door_point[0], door_point[1])
        dis_set.append(dis)
  
    return dis_set

# dis_set = distance([9.044], [3.0366], TOP_EXIT) #(16420,30852)
# print(dis_set)

def exitTime(dis, front_people_num):
    #TODO 门宽
    return dis / Velocity + front_people_num / (CPeople * WidthDoor)

def compareDis(cur_dis,select_door_dis_array,local):
    dis_count = 0
    dis_list = sorted(select_door_dis_array.items(), key=lambda x: x[1][local])
    for item in dis_list:
        dis = item[1][local]
        
        if cur_dis < dis:
            # print(dis_count,cur_dis,dis)
            break
        dis_count += 1
    return dis_count


def init_iteration(dict_dis):
    print('初始化人员选择出口')
    global dict_select_door_top
    global dict_select_door_bottom
    global dict_select_door_left  
    global dict_select_door_right

    for key in dict_dis:
        item = dict_dis[key]
        # 比较距离
        min_value = np.min(item)
        index = item.index(min_value)

        people_select.append(index)
        if index == 0:
            dict_select_door_top[key] = item
            # print('index0',len(dict_select_door_top))
        elif index == 1:
            dict_select_door_bottom[key] = item
            # print('index1',len(dict_select_door_bottom))
        elif index == 2:
            dict_select_door_left[key] = item
            # print('index2',len(dict_select_door_left))
        elif index == 3:
            dict_select_door_right[key] = item
            # print('index3',len(dict_select_door_right))
    # print('dict_select_door_right',dict_select_door_right)
    print(len(dict_select_door_top),len(dict_select_door_bottom),len(dict_select_door_left),len(dict_select_door_right))
    return dict_select_door_top,dict_select_door_bottom,dict_select_door_left, dict_select_door_right


def init_time():
    global array_select_door_top_time
    global array_select_door_bottom_time
    global array_select_door_left_time
    global array_select_door_right_time
    global dict_select_door_top
    global dict_select_door_bottom
    global dict_select_door_left
    global dict_select_door_right

    for key in dict_select_door_top:
        item = dict_select_door_top[key]
        num_top = compareDis(item[0],dict_select_door_top,0)
        array_select_door_top_time[key] = exitTime(item[0],num_top)

    for key in dict_select_door_bottom:
        item = dict_select_door_bottom[key]
        num_bottom = compareDis(item[1],dict_select_door_bottom,1)
        array_select_door_bottom_time[key] = exitTime(item[1], num_bottom)

    for key in dict_select_door_left:
        item = dict_select_door_left[key]
        num_left = compareDis(item[2],dict_select_door_left,2)
        array_select_door_left_time[key] = exitTime(item[2],num_left)

    for key in dict_select_door_right:
        item = dict_select_door_right[key]
        num_right = compareDis(item[3],dict_select_door_right,3)
        array_select_door_right_time[key] = exitTime(item[3], num_right)





def iteration():
    global finished_time
    global count
    global dict_dis
    global dict_select_door_top
    global dict_select_door_bottom
    global dict_select_door_left
    global dict_select_door_right

    global array_select_door_top_time
    global array_select_door_bottom_time
    global array_select_door_left_time
    global array_select_door_right_time


    for key in dict_dis:
    	item = dict_dis[key]

        num_top = compareDis(item[0],dict_select_door_top,0)
        num_bottom = compareDis(item[1],dict_select_door_bottom,1)
        num_left = compareDis(item[2],dict_select_door_left,2)
        num_right = compareDis(item[3],dict_select_door_right,3)


        people_to_top_time = exitTime(item[0],num_top)
        people_to_bottom_time = exitTime(item[1],num_bottom)
        people_to_left_time = exitTime(item[2],num_left)
        people_to_right_time = exitTime(item[3],num_right)

        timeArray = []
        timeArray.append(people_to_top_time)
        timeArray.append(people_to_bottom_time)
        timeArray.append(people_to_left_time)
        timeArray.append(people_to_right_time)


       	min_time = np.min(timeArray)
        index = timeArray.index(min_time)
        people_select_num = people_select[key]
        
        if(people_select_num != index):
            
            print('label',label[key],'item:',item)
            print('timeArray',timeArray)
            print('key:',key,'people_select_num',people_select_num,'==>>index:',index)
        
            print('distance before',len(dict_select_door_top),len(dict_select_door_bottom),len(dict_select_door_left), len(dict_select_door_right))
            print('time before',len(array_select_door_top_time),len(array_select_door_bottom_time),len(array_select_door_left_time), len(array_select_door_right_time))
            
            #删除原始位置
            
            if people_select_num == 0:
                del dict_select_door_top[key]  
                del array_select_door_top_time[key]

            elif people_select_num == 1:
                del dict_select_door_bottom[key]
                del array_select_door_bottom_time[key]

            elif people_select_num == 2:
                del dict_select_door_left[key]
                del array_select_door_left_time[key] 

            elif people_select_num == 3:
                del dict_select_door_right[key]
                del array_select_door_right_time[key]

            #移动到对应的门
            people_select[key] = index
            if index == 0:
                dict_select_door_top[key] = item
                array_select_door_top_time[key] = people_to_top_time
            elif index == 1:
                
                dict_select_door_bottom[key] = item
                array_select_door_bottom_time[key] = people_to_bottom_time
            elif index == 2:
         
                dict_select_door_left[key] = item
                array_select_door_left_time[key] = people_to_left_time
            elif index == 3:
            
                dict_select_door_right[key] = item
                array_select_door_right_time[key] = people_to_right_time
        
            print('distance after',len(dict_select_door_top),len(dict_select_door_bottom),len(dict_select_door_left), len(dict_select_door_right))
            print('time after',len(array_select_door_top_time),len(array_select_door_bottom_time),len(array_select_door_left_time), len(array_select_door_right_time))
           
    # return 'success'

    # a = sorted(array_select_door_top_time.items(), key=lambda x: x[1])
    # b = sorted(array_select_door_bottom_time.items(), key=lambda x: x[1])
    # c = sorted(array_select_door_left_time.items(), key=lambda x: x[1])
    # d = sorted(array_select_door_right_time.items(), key=lambda x: x[1])
    a = array_select_door_top_time.values()
    b = array_select_door_bottom_time.values()
    c = array_select_door_left_time.values()
    d = array_select_door_right_time.values()

    print('iteration',count+1,'after',len(array_select_door_top_time),len(array_select_door_bottom_time),len(array_select_door_left_time), len(array_select_door_right_time))
    finished_time = [max(a),max(b),max(c),max(d)]
    print('======================time max===============',finished_time)
    
   
    count += 1
    if count > max_count:
        return max_count
    else:
        print('===============================完成一次迭代===========================')
        print('iteration_count',count)
        return iteration()


def classification():
    global dict_select_door_top
    global dict_select_door_bottom
    global dict_select_door_left
    global dict_select_door_right
    global dict_point
    
    global select_top_x
    global select_top_y
    global select_bottom_x
    global select_bottom_y
    global select_left_x
    global select_left_y
    global select_right_x
    global select_right_y

    print(len(dict_select_door_top))
    print(len(dict_select_door_bottom))
    print(len(dict_select_door_left))
    print(len(dict_select_door_right))

    
    # print(dict_point)
    # 
    
    for key in dict_select_door_top:
        item = dict_point[key]
        select_top_x.append(item[0])
        select_top_y.append(item[1])

    for key in dict_select_door_bottom:
        item = dict_point[key]
        select_bottom_x.append(item[0])
        select_bottom_y.append(item[1])

    for key in dict_select_door_left:
        item = dict_point[key]
        select_left_x.append(item[0])
        select_left_y.append(item[1])

    for key in dict_select_door_right:
        item = dict_point[key]
        select_right_x.append(item[0])
        select_right_y.append(item[1])

    # print(select_top_x,select_top_y)
    # print(select_bottom_x,select_bottom_y)
    # print(select_left_x,select_left_y)
    # print(select_right_x,select_right_y)


def seatPoint():
    x = []
    y = []
    global label
    #读取座位
    x_zw = []
    y_zw = []
    label_zw = []
    with open('point_zw.csv', 'rb') as f:        # 采用b的方式处理可以省去很多问题
        reader = csv.reader(f)
        # print(type(reader))
        for row in reader:
            # do something with row, such as row[0],row[1]
            if row[1] != 'x':
                x_zw.append(row[1])
                y_zw.append(row[2])
                label_zw.append(row[0])

                float_x = float(row[1])
                float_y = float(row[2])
                x_m = float_x/1000
                y_m = float_y/1000
                # print(x_m,y_m)
                x.append(x_m)
                y.append(y_m)
                label.append(row[0])
    return x,y

def otherPoint():
    ##读取通道
    x_td = []
    y_td = []
    label_td = []
    with open('point_td.csv', 'rb') as f:        # 采用b的方式处理可以省去很多问题
        reader = csv.reader(f)
        # print(type(reader))
        for row in reader:
            # do something with row, such as row[0],row[1]
            if row[1] != 'x':
                float_x = float(row[1])
                float_y = float(row[2])
                x_m = float_x/1000
                y_m = float_y/1000
                # print(x_m,y_m)
                x_td.append(x_m)
                y_td.append(y_m)

                label_td.append(row[0])
                # plt.text(row[1],row[2],str(row[0]), family='serif', style='italic', ha='right', wrap=True)
                # print(row[1],row[2])
    ##读取楼梯
    x_lt = []
    y_lt = []
    label_lt = []
    with open('point_lt.csv', 'rb') as f:        # 采用b的方式处理可以省去很多问题
        reader = csv.reader(f)
        # print(type(reader))
        for row in reader:
            # do something with row, such as row[0],row[1]
            if row[1] != 'x':
                float_x = float(row[1])
                float_y = float(row[2])
                x_m = float_x/1000
                y_m = float_y/1000
                # print(x_m,y_m)
                x_lt.append(x_m)
                y_lt.append(y_m)

                label_lt.append(row[0])
                # plt.text(row[1],row[2],str(row[0]), family='serif', style='italic', ha='right', wrap=True)
                # print(row[1],row[2])
    ##读取辅助点
    x_fz = []
    y_fz = []
    label_fz = []
    with open('point_node.csv', 'rb') as f:        # 采用b的方式处理可以省去很多问题
        reader = csv.reader(f)
        # print(type(reader))
        for row in reader:
            # do something with row, such as row[0],row[1]
            if row[1] != 'x':

                float_x = float(row[1])
                float_y = float(row[2])
                x_m = float_x/1000
                y_m = float_y/1000
                # print(x_m,y_m)
                x_fz.append(x_m)
                y_fz.append(y_m)
                label_fz.append(row[0])

    return x_td,y_td,label_td,x_lt,y_lt,label_lt,x_fz,y_fz,label_fz

if __name__ == '__main__':

    # test  = True
    test  = False
    if test :
        print('==========================================test==========================================')
        dict_seat,arr_seat = getAllSeatDis()

        a = np.array(arr_seat)
        top_door_distance_set = a[:,0]
        bottom_door_distance_set = a[:,1]
        left_door_distance_set = a[:,2]
        right_door_distance_set = a[:,3]

        print(top_door_distance_set[0:20])
        print(bottom_door_distance_set[0:20])
        print(left_door_distance_set[0:20])
        print(right_door_distance_set[0:20])



    else:
        x,y = seatPoint()
        #清洗数据
        x,y = fiterPoint(x,y)

        print('x:', len(x))
        print('y:', len(y))

        #获取每个点到四个门的距离
        #TODO 这里后面需要用最短距离
        dict_seat,arr_seat = getAllSeatDis()

        a = np.array(arr_seat)
        top_door_distance_set = a[:,3]
        bottom_door_distance_set = a[:,1]
        left_door_distance_set = a[:,0]
        right_door_distance_set = a[:,2]
        # print('distance to all door',len(top_door_distance_set),len(bottom_door_distance_set),len(left_door_distance_set), len(right_door_distance_set))
        # 
        # top_door_distance_set = distance(x, y, TOP_EXIT)
        # bottom_door_distance_set = distance(x, y, BOTTOM_EXIT)
        # left_door_distance_set = distance(x, y, LEFT_EXIT)
        # right_door_distance_set = distance(x, y, RIGHT_EXIT)
        

        #把坐标和距离都转化成字典
        #{i:[上、下、左、右]}
        for i in range(len(x)):

            dict_dis[i] = [top_door_distance_set[i],bottom_door_distance_set[i],left_door_distance_set[i], right_door_distance_set[i]]
            dict_point[i] = [x[i], y[i]]

        print('distance to all door',len(top_door_distance_set),len(bottom_door_distance_set),len(left_door_distance_set), len(right_door_distance_set))

        #按照距离选择门口
        init_iteration(dict_dis)
        

        #根据距离选择门需要的时间
        init_time()
        print('---------------开始迭代-----------')
        step = iteration()
        classification()

        print('iteration', step)
        

        #获取通道节点 楼梯 通道 辅助节点
        x_td,y_td,label_td,x_lt,y_lt,label_lt,x_fz,y_fz,label_fz = otherPoint()
        


        fig = plt.figure(figsize=(80, 56), dpi=50)
        # # print(len(select_right_x),len(select_right_y))
        plt.plot(x_td,y_td,'ro',color='magenta',label='Exit')
        plt.plot(x_lt,y_lt,'ro',color='black',label='stair')
        # plt.plot(x_lt,y_lt,'ro',color='black',label='stair')

      
        plt.plot(select_top_x,select_top_y,'ro',color='blue',label=str('exit_top'+'time:'+finished_time[0]+'s'))
        plt.plot(select_bottom_x,select_bottom_y,'ro',color='green',label=str('exit_bottom'+'time:'+finished_time[1]+'s'))
        plt.plot(select_left_x,select_left_y,'ro',color='red',label=str('exit_left'+'time:'+finished_time[2]+'s'))
        plt.plot(select_right_x,select_right_y,'ro',color='yellow',label=str('exit_right'+'time:'+finished_time[3]+'s'))


        plt.xlim(0, 60)
        plt.ylim(0, 40)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('evacuation')
        plt.legend()
        plt.grid(True)
        plt.savefig('image.png')
        plt.show()






