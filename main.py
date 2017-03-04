#coding:utf-8

import numpy as np
import matplotlib.pyplot as plt



count = 0
x = []
y = []
samply_left, samply_right = 300, 600
pre_room_len, pre_room_width = 20, 10
left_door_distance_set =[]
right_door_distance_set = []

select_left = []
select_right = []
people_select = []

#选择出口行人和门的距离
select_left_dis = []
select_right_dis = []


Velocity = 1 #m/s
Num =[]
WidthDoor = 0.5
CPeople = 1.33 #m/s

def compareDis(cur_dis,dis_set):
    dis_set.append(cur_dis)
    dis_set.sort()
    return dis_set.index(cur_dis)

def calDoorDistance(x1,y1,x2,y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


def exitTime(dis,front_people_num):
    return dis/Velocity + front_people_num/(CPeople*WidthDoor)


def distance(people_x, people_y, door_x, door_y):

    dis_set = []
    lenght = len(people_x)
    # print(lenght)
    for item in range(lenght):
        # print(item)
        dis = calDoorDistance(people_x[item], people_y[item], door_x, door_y)
        dis_set.append(dis)
    # if door_loc == 'left':
    #     left_door_distance_set = dis_set
    # else:
    #     right_door_distance_set = dis_set
    return dis_set

def init_iteration(left,right):
    global select_left_dis
    global select_right_dis
    #select_left = []
    #select_right = []
    for item in range(900):
        if left[item] < right[item]:
            #select_left.append(left[item])
            people_select.append(0)
            select_left_dis.append(left[item])

        else:
            #select_right.append(right[item])
            people_select.append(1)
            select_right_dis.append(right[item])


    select_left_dis.sort()
    select_right_dis.sort()
    print(len(select_left_dis),len(select_right_dis))
    return select_left_dis,select_right_dis

def satar_iteration(left,right):
    global count
    global people_select
    global select_left_dis
    global select_right_dis

    front_people_num_left = 0
    front_people_num_right = 0
    iteration_set=[]

    people_select_set = []
    select_left_dis_set = []
    select_right_dis_set = []

    for item in range(900):
        dis_left = left[item]  # 到左边门的距离
        dis_right = right[item]  # 到右边门的距离

        if people_select[item] == 0 : #选择左边的门
            #计算离门小于该人员的距离的总人数
            front_people_num_left = select_left_dis.index(dis_left)
            front_people_num_right = compareDis(dis_right, select_right_dis)
            print('当前是 左 人数：', front_people_num_left, front_people_num_right,dis_left,dis_right,x[item],y[item])

        else: #选择右边的门
            #计算离门小于该人员的距离的总人数
            front_people_num_right = select_right_dis.index(dis_right)
            front_people_num_left = compareDis(dis_left,select_left_dis)
            print('当前是 右 人数：', front_people_num_left, front_people_num_right,dis_left,dis_right, x[item],y[item])

        #计算时间

        left_time = exitTime(dis_left, front_people_num_left)
        right_time = exitTime(dis_right, front_people_num_right)

        #选择时间较短的出口
        if left_time < right_time :
            #存储改点的距离
            select_left_dis_set.append(dis_left)
            #标记选择的出口
            people_select_set.append(0)
        else:
            select_right_dis_set.append(dis_right)
            people_select_set.append(1)
    #更新选择出口的全局存储
    select_left_dis = select_left_dis_set.sort()
    select_right_dis = select_right_dis_set.sort()
    people_select = people_select_set
    count = count + 1
    print('迭代:',count,len(select_left_dis_set),len(select_right_dis_set))
    # satar_iteration(left, right)


if __name__ == '__main__':

    a = [1, 2, 3]
    b = [4, 5, 6,7]
    c= a+b
    print(c)
    left_num_x = np.random.random(size=samply_left)
    left_num_y = np.random.random(size=samply_left)
    right_num_x  = np.random.random(size=samply_right)
    right_num_y = np.random.random(size=samply_right)
    # print(left_num)
    x_l = pre_room_width * left_num_x + 0
    y_l = pre_room_len * left_num_y + 0


    x_r = pre_room_width * right_num_x + 10
    y_r = pre_room_len * right_num_y + 0

    # print(len(x_l))
    # print(len(x_r))

    x = np.append(x_l,x_r)

    y = np.append(y_l,y_r) #y_l+y_r[0:300]


    print('x:',len(x))
    print('y:',len(y))
    left_door_distance_set = distance(x, y, 5, 0)
    right_door_distance_set = distance(x, y, 15, 0)


    print(len(left_door_distance_set),len(right_door_distance_set))

    init_iteration(left_door_distance_set,right_door_distance_set)

    satar_iteration(left_door_distance_set,right_door_distance_set)

    # print(select_left_dis[0:10],select_right_dis[0:10])
    # print(left_door_distance_set[0:11], right_door_distance_set[0:11])
    # print(left_door_distance_set[10], right_door_distance_set[10])
    plt.figure(figsize=(20, 20), dpi=50)
    plt.plot(x_l, y_l, 'ro')
    plt.plot(x_r, y_r, 'ro')
    plt.xlim(0, 20)
    plt.ylim(0, 20)
    plt.xlabel('x 20m')
    plt.ylabel('y 20m')
    plt.title('liangshihua')
    plt.grid(True)
    plt.savefig('imag.png')
    plt.show()









