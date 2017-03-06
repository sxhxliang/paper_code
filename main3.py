# coding:utf-8

import numpy as np
import matplotlib.pyplot as plt

count = 0

max_count = 150
x = []
y = []
samply_left, samply_right = 300, 600
pre_room_len, pre_room_width = 20, 10
left_door_distance_set = []
right_door_distance_set = []

select_left_x = []
select_left_y = []

select_right_x = []
select_right_y = []
people_select = []

# 选择出口行人和门的距离
select_left_dis = []
select_right_dis = []
# 左右两门疏散的时间
# door_left_time, door_right_time = 0, 0
# 人员距离字典
dict_dis = {}
# 人员坐标字典
dict_point = {}
# 选择左门的字典
dict_select_door_left = {}
dict_select_door_right = {}
# # 用于时间排序
array_select_door_left_time = {}
array_select_door_right_time = {}

#用于标记左右两门完全疏散时间
# exit_left_time = 0
# exit_right_time =0


Velocity = 1  # m/s
Num = []
WidthDoor = 0.5
CPeople = 1.33  # m/s
def delPoint(px,py,arr_len,count):
    xi = np.random.randint(0, count)
    px[xi] = None
    py[xi] = None
    x,y=fiterPoint(px, py)
    if len(x) > arr_len:
        return delPoint(x,y,arr_len,len(x)-1)
    else:
        return x,y


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
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


def exitTime(dis, front_people_num):
    return dis / Velocity + front_people_num / (CPeople * WidthDoor)


def compareRightDis(cur_dis):
    dis_count = 0
    global dict_select_door_right
    global dict_dis_right
    dict_dis_right = sorted(dict_select_door_right.items(), key=lambda x: x[1][1])
    for item in dict_dis_right:
        right = item[1][1]
        # print(cur_dis,right)
        if cur_dis < right:
            break
        dis_count += 1
    return dis_count


def compareLeftDis(cur_dis):
    dis_count = 0
    global dict_select_door_left
    global dict_dis_left

    dict_dis_left = sorted(dict_select_door_left.items(), key=lambda x: x[1][0])
    # print('compareDis:', cur_dis, position, len(dict_dis))
    # print(dict_dis_left[0:3])
    for item2 in dict_dis_left:
        left = item2[1][0]
        # print(cur_dis,left)
        if cur_dis < left:
            break
        dis_count += 1
    return dis_count





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



def init_iteration(dict_dis):
    print('初始化人员选择出口')
    global dict_select_door_right
    global dict_select_door_left

    for key in dict_dis:
        item = dict_dis[key]
        # 比较距离
        if item[0] < item[1]:
            people_select.append(0)
            dict_select_door_left[key] = item


        else:
            people_select.append(1)
            dict_select_door_right[key] = item

    # print('dict_select_door_right',dict_select_door_right)
    return dict_select_door_left, dict_select_door_right


def init_time():
    global array_select_door_left_time
    global array_select_door_right_time

    global dict_select_door_right
    global dict_select_door_left

    for key in dict_select_door_left:
        # print(key)
        item = dict_select_door_left[key]
        num_left = compareRightDis(item[0])

        array_select_door_left_time[key] = exitTime(item[0],num_left)
        # print(item)


    for key in dict_select_door_right:
        item = dict_select_door_right[key]
        num_right = compareRightDis(item[1])
        array_select_door_right_time[key] = exitTime(item[0], num_right)





def iteration():
    global count
    global dict_dis
    global dict_select_door_left
    global dict_select_door_right
    global array_select_door_left_time
    global array_select_door_right_time

    for key in dict_dis:

        peple_left_num = compareLeftDis(dict_dis[key][0])
        people_right_num = compareRightDis(dict_dis[key][1])

        people_to_left_time = exitTime(dict_dis[key][0],peple_left_num)
        people_to_right_time = exitTime(dict_dis[key][0],people_right_num)


        if people_to_left_time < people_to_right_time:
            if people_select[key] == 1:
                # print('右到左')
                people_select[key] = 0
                dict_select_door_left[key] = dict_dis[key]
                array_select_door_left_time[key] = people_to_left_time
                del array_select_door_right_time[key]
                del dict_select_door_right[key]

        else:
            if people_select[key] == 0:
                # print('左到右')
                people_select[key] = 1
                dict_select_door_right[key] = dict_dis[key]
                array_select_door_right_time[key] = people_to_right_time
                del array_select_door_left_time[key]
                del dict_select_door_left[key]
    a = sorted(array_select_door_left_time.items(), key=lambda x: x[1], reverse=True)
    b = sorted(array_select_door_right_time.items(), key=lambda x: x[1], reverse=True)
    count += 1
    if count > max_count:
        return 150
    else:
        print('迭代',count)
        return iteration()


def classification():
    global dict_select_door_left
    global dict_select_door_right
    global dict_point
    #
    global select_right_x
    global select_right_y
    global select_left_x
    global select_left_y
    print(len(dict_select_door_left))
    print(len(dict_select_door_right))
    # print(dict_point)
    for key in dict_select_door_left:
        # print(key)
        item = dict_point[key]
        # print(item)
        select_left_x.append(item[0])
        select_left_y.append(item[1])

    for key in dict_select_door_right:
        item = dict_point[key]
        select_right_x.append(item[0])
        select_right_y.append(item[1])

        # print(len(select_left_x))
        # print(len(select_right_x))


if __name__ == '__main__':

    # a = [1, 2, 3]
    # b = [4, 5, 6,7]
    # d = {1:[1,2],3:[3,4]}
    # # c= a+b
    # print(d.keys())
    point_left_x = []
    point_left_y = []
    point_right_x = []
    point_right_y = []

    for xi in range(20):
        px = xi * 0.5 + 0.25

        for yi in range(40):
            py = yi * 0.5 + 0.25
            point_left_x.append(px)
            point_left_y.append(py)

    for xi in range(20):
        px = xi * 0.5 + 10.25
        for yi in range(40):
            py = yi * 0.5 + 0.25
            point_right_x.append(px)
            point_right_y.append(py)



    print(len(point_left_x))
    print(len(point_left_y))
    print(len(point_right_x))
    print(len(point_right_y))

    # for d in range(500):
    #     # print(d)
    #     # num = 799 - d
    #     xi = np.random.randint(0, 799)
    #     point_left_x[xi] = None
    #     point_left_y[xi] = None
    #
    # for d in range(200):
    #     # num = 799 - d
    #     xi = np.random.randint(0, 799)
    #     point_right_x[xi] = None
    #     point_right_y[xi] = None
    point_left_x, point_left_y = delPoint(point_left_x, point_left_y, 300, 800)
    point_right_x, point_right_y = delPoint(point_right_x, point_right_y,600,800)



    # print('point_right_x:',len(point_right_x))

    # left_num_x = np.random.random(size=samply_left)
    # left_num_y = np.random.random(size=samply_left)
    # right_num_x = np.random.random(size=samply_right)
    # right_num_y = np.random.random(size=samply_right)
    # # print(left_num)
    # x_l = pre_room_width * left_num_x + 0
    # y_l = pre_room_len * left_num_y + 0
    #
    # x_r = pre_room_width * right_num_x + 10
    # y_r = pre_room_len * right_num_y + 0
    #
    # # print(len(x_l))
    # # print(len(x_r))
    #
    x = np.append(point_left_x, point_right_x)
    #
    y = np.append(point_left_y, point_right_y)  # y_l+y_r[0:300]

    x,y = fiterPoint(x,y)

    print('x:', len(x))
    print('y:', len(y))

    left_door_distance_set = distance(x, y, 5, 0)
    right_door_distance_set = distance(x, y, 15, 0)

    for i in range(samply_left + samply_right):
        dict_dis[i] = [left_door_distance_set[i], right_door_distance_set[i]]

        dict_point[i] = [x[i], y[i]]

    # print(dict_point,len(dict_point))
    print(len(left_door_distance_set), len(right_door_distance_set))

    init_iteration(dict_dis)
    init_time()
    print('---------------开始迭代-----------')
    step = iteration()
    classification()

    print('迭代', step)
    #


    # for i in range(200):
    #     res,_ = satar_iteration(left_door_distance_set,right_door_distance_set)
    #     if res == 0:
    #         print('迭代完成')
    #         break



    # print(select_left_dis[0:10],select_right_dis[0:10])
    # print(left_door_distance_set[0:11], right_door_distance_set[0:11])
    # print(left_door_distance_set[10], right_door_distance_set[10])
    fig = plt.figure(figsize=(20, 20), dpi=50)
    # window = fig.add_subplot(111)
    plt.scatter(select_left_x, select_left_y, s=20, c='blue')
    plt.scatter(select_right_x, select_right_y, s=20, c='red')
    # print(len(select_right_x),len(select_right_y))
    # plt.plot(x, y, 'ro')
    plt.xlim(0, 20)
    plt.ylim(0, 20)
    plt.xlabel('x 20m')
    plt.ylabel('y 20m')
    plt.title('evacuation')
    plt.grid(True)
    plt.savefig('imag.png')
    plt.show()









