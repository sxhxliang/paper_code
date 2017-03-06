# coding:utf-8

import numpy as np
import matplotlib.pyplot as plt

count = 0

max_count = 300
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
door_left_time, door_right_time = 0, 0
# 人员距离字典
dict_dis = {}
# 人员坐标字典
dict_point = {}
# 选择左门的字典
dict_select_door_left = {}
dict_select_door_right = {}
# # 用于时间排序
# dict_select_door_left_time = {}
# dict_select_door_right_time = {}

Velocity = 1  # m/s
Num = []
WidthDoor = 0.5
CPeople = 1.33  # m/s

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


# 得到选择左门每个人的时间字典
def calLeftPeoPleTime():
    global dict_select_door_left

    print(len(dict_select_door_left))
    dict_select_door_left_time = {}

    d = sorted(dict_select_door_left.items(), key=lambda x: x[1][0])

    # print(d)
    for i in range(len(d)):
        item = d[i]
        people_id = item[0]
        time = exitTime(item[1][0], i)
        dict_select_door_left_time[people_id] = time

    return dict_select_door_left_time


# 得到选择右门每个人的时间字典
def calRightPeoPleTime():
    global dict_select_door_right
    dict_select_door_right_time = {}
    print(len(dict_select_door_right))


    d = sorted(dict_select_door_right.items(), key=lambda x: x[1][0])

    for i in range(len(d)):
        item = d[i]
        people_id = item[0]
        time = exitTime(item[1][1], i)
        dict_select_door_right_time[people_id] = time

    # print(dict_select_door_right_time)
    print('得到选择右门每个人的时间字典', len(dict_select_door_right_time))
    return dict_select_door_right_time


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


def iteration_left():
    global dict_select_door_left
    global dict_select_door_right
    global door_left_time

    # print('test',dict_select_door_left)

    leftPeoPleTime = calLeftPeoPleTime()
    print('时间list',len(leftPeoPleTime))

    time = sorted(leftPeoPleTime.items(), key=lambda x: x[1], reverse=True)
    people_id = time[0][0]
    people_time = time[0][1]

    people_to_right_dis = dict_select_door_left[people_id][1]
    people_to_right_num = compareRightDis(people_to_right_dis)
    people_to_right_time = exitTime(people_to_right_dis, people_to_right_num)

    print('iteration_left-最长时间：',people_time,'people_to_right_time',people_to_right_time)
    if people_time > people_to_right_time:
        print('左人移去右门')
        door_left_time = people_time
        dict_select_door_right[people_id] = dict_select_door_left[people_id]
        del dict_select_door_left[people_id]

    return people_time


def iteration_right():
    global dict_select_door_left
    global dict_select_door_right
    global door_right_time
    global count
    rightPeoPleTime = calRightPeoPleTime()
    time = sorted(rightPeoPleTime.items(), key=lambda x: x[1], reverse=True)
    print(time[0])

    people_id = time[0][0]
    people_time = time[0][1]

    # print(dict_select_door_right)
    print('people_id',people_id)
    people_to_left_dis = dict_dis[people_id][0]
    # print('people_to_left_dis',people_to_left_dis)

    # people_to_left_dis[0]

    people_to_left_num = compareLeftDis(people_to_left_dis)
    people_to_left_time = exitTime(people_to_left_dis, people_to_left_num)
    print('iteration_right，最长时间',people_time,'people_to_left_time',people_to_left_time)

    if people_time > people_to_left_time:
        print('右人移去左门',people_id,'count',count)

        door_right_time = people_time
        # print(dict_select_door_right)
        dict_select_door_left[people_id] = dict_select_door_right[people_id]
        del dict_select_door_right[people_id]

    return people_time


def iteration2():
    global count
    time1 = iteration_left()
    time2 = iteration_right()

    count += 1
    print('迭代次数：',count)
    # 比较两门的时间
    if time1 < time2:
        print('左边花费时间：', time1, '右边花费时间', time2)
        if count > max_count:
            return 300
        else:
            return iteration2()
    else:
        return count

#
# def iteration():
#     # global dict_dis
#     global dict_select_door_left
#     global dict_select_door_right
#     global count
#     global door_left_time
#     global door_right_time
#
#     # 一、找到疏散时间最长的门，
#     # 0给选择左门的字典按照左门距离排序
#     b = sorted(dict_select_door_left.items(), key=lambda x: x[1][0], reverse=True)
#     # print(b)
#     # 1.找到选择这个门有多少人
#     left_num1 = len(b) - 1
#
#     # 2 找到离这个门最远的人（距离，和ID）
#     people_dis = b[0][1][0]
#     people_id = b[0][0]
#
#     print('左人坐标', x[people_id], y[people_id])
#
#     # 3.计算时间这个人到左门的距离
#     time_left1 = exitTime(people_dis, left_num1)
#     door_left_time = time_left1
#     print('左人，左门：', time_left1, 's', '前面人数:', left_num1, '到左右门的距离:', b[0][1])
#     # 4.找到这个人和右门的距离和选择右门的人数
#     people_dis = b[0][1][1]
#     left_num2 = compareRightDis(people_dis)
#     # print('左人，右门，人数',left_num2)
#     # 计算到右门时间
#
#     time_left2 = exitTime(people_dis, left_num2)
#     print('左人，右门：', time_left2, 's', '前面人数', left_num2, '到左右门的距离:', b[0][1])
#
#     if time_left1 > time_left2:
#         print('左人移去右门')
#         door_left_time = time_left1
#         dict_select_door_right[people_id] = dict_select_door_left[people_id]
#         del dict_select_door_left[people_id]
#     else:
#         door_left_time = time_left2
#
#     # print(b[0])
#     # print(people_dis)
#     # print('选择左门，左右门时间：',time_left1,time_left2)
#     #
#
#     # -----------------------------------------选择右门
#
#
#     # 二、计算到右边的门的最长时间
#     b = sorted(dict_select_door_right.items(), key=lambda x: x[1][1], reverse=True)
#     right_num1 = len(b) - 1
#     people_dis = b[0][1][1]
#     people_id = b[0][0]
#
#     print('右人坐标', x[people_id], y[people_id])
#     # 选择右门的人到右门的时间
#     time_right1 = exitTime(people_dis, right_num1)
#
#     print('右人，右门：', time_right1, 's', '前面人数:', right_num1, '到左右门的距离:', b[0][1])
#     # door_right_time = time_right1
#     # 右门的人选择左门的人数和时间
#     people_dis = b[0][1][0]
#     # print('右-左',people_dis)
#     right_num2 = compareLeftDis(people_dis)
#
#     time_right2 = exitTime(people_dis, right_num2)
#
#     print('右人，左门：', time_right2, 's', '前面人数:', right_num2, '到左右门的距离:', b[0][1])
#
#     if time_right1 > time_right2:
#         print('右人移去左门')
#         door_right_time = time_right1
#         dict_select_door_left[people_id] = dict_select_door_right[people_id]
#         del dict_select_door_right[people_id]
#     else:
#         door_right_time = time_right2
#
#     # 迭代计数
#     count += 1
#     print(count)
#     print('选择左右门的人数分别为', len(dict_select_door_left), len(dict_select_door_right))
#
#     # 根据更新后的选择重新计算时间
#
#
#     #
#
#     # 比较两门的时间
#     if time_left1 < time_right1:
#         if count > max_count:
#             return 300
#         else:
#             return iteration()
#     else:
#         return count
#
#
#
#         # 计算把这个人分配到其他n-1各门时，
#
#         # 每个门新的疏散时间，这样有n个疏散时间，
#         # 找出最短的一个，把这个人调整到最短时间的方案上
#

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
    left_num_x = np.random.random(size=samply_left)
    left_num_y = np.random.random(size=samply_left)
    right_num_x = np.random.random(size=samply_right)
    right_num_y = np.random.random(size=samply_right)
    # print(left_num)
    x_l = pre_room_width * left_num_x + 0
    y_l = pre_room_len * left_num_y + 0

    x_r = pre_room_width * right_num_x + 10
    y_r = pre_room_len * right_num_y + 0

    # print(len(x_l))
    # print(len(x_r))

    x = np.append(x_l, x_r)

    y = np.append(y_l, y_r)  # y_l+y_r[0:300]

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
    print('---------------开始迭代-----------')
    step = iteration2()
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
    # plt.plot(x_r, y_r, 'ro')
    plt.xlim(0, 20)
    plt.ylim(0, 20)
    plt.xlabel('x 20m')
    plt.ylabel('y 20m')
    plt.title('evacuation')
    plt.grid(True)
    plt.savefig('imag.png')
    plt.show()









