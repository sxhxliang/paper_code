# coding:utf-8
import os
import numpy as np

# import matplotlib.pyplot as plt

#读取csv文件
#
import csv
import math
from node import calDistance,get_node
from astar import getAllNodeDis


SEAT_NEAR = ['null','A','t_1','B','F_1','C','t_2','D','t_3','null','E','t_4','F','t_5','G','null','H','t_6','I','F_2','J','t_7','t_8','K','t_9','null','L','t_10','M','t_11','N','null']
# 各个节点的信息
# {'t_1_1':{'coord':(12,22),'id':0},'t_1_2':{'coord':(5,12),'id':1},'t_1_3':{'coord':(6,8),'id':2},'t_1_4':{'coord':(1,12),'id':3},'t_1_5':{'coord':(1,18),'id':4},'F_1_1':{'coord':(15,12),'id':5},'F_1_2':{'coord':(15,22),'id':6}}
dict_node = get_node() 
#各个节点最短距离
#{'F_2_3': [{'route': ['td_1', 'F_2_1', 'F_2_2', 'F_2_3'], 'route_dis': 38.46198258839964}, {'route':..}]},{..}}
all_node_dis = getAllNodeDis()
dict_seat = {}

TOP_EXIT = (16.420,30.852)
BOTTOM_EXIT = (34.720,6.587)
LEFT_EXIT = (6.565,18.720)
RIGHT_EXIT = (43.875,18.720)

EXIT_NODE = [LEFT_EXIT,BOTTOM_EXIT,RIGHT_EXIT,TOP_EXIT]

def get_seat():
	node = {}
	with open('point_zw.csv', 'rb') as f:        # 采用b的方式处理可以省去很多问题
		reader = csv.reader(f)
		i = 0
		for row in reader:

			if row[1] != 'x':

				item = {}

				float_x = float(row[1])
				float_y = float(row[2])
				x_m = float_x/1000
				y_m = float_y/1000

				item['id'] = (i)
				item['coord'] = (x_m,y_m)

				i+=1
				node[row[0]] = item

	return node



dict_seat = get_seat()
dict_seat_arr = sorted(dict_seat.items(), key=lambda x: x[1]['id'])

def getAllSeatDis():
	global dict_node_arr
	global dict_seat_arr
	SeatDis = {}
	seat_dis_arr = []


	# for i in range(12):
	for i in range(len(dict_seat_arr)):
		#存某个座位到四个出口的最短路径
		seat_dis = []
		# print('dict_seat_arr',dict_seat_arr)
		coord = dict_seat_arr[i][1]['coord']

		label = dict_seat_arr[i][0]
		l_arr = label.split('_')
		l_index = SEAT_NEAR.index(l_arr[0])

		pre_node = SEAT_NEAR[l_index-1]
		next_node = SEAT_NEAR[l_index+1]

		seat_pre_node_to_four_exit = [100,100,100,100]
		seat_next_node_to_four_exit = [100,100,100,100]
		dis_to_exit = []

		# 判断是不是在第一排，A_1_1
		if int(l_arr[1]) == 1:
			for x in range(4):
				exit_coord = EXIT_NODE[x]
				dis_to_exit.append(calDistance(coord,exit_coord))

		else:
		
			if pre_node !='null':
				#同一排节点
				pre_node_label = pre_node + '_' + l_arr[1]
				
				dis_to_pre_node = calDistance(coord,dict_node[pre_node_label]['coord'])
				# 计算路径
				route = all_node_dis[pre_node_label]
				
				for i in range(len(route)):
					item = route[i]
					# i = {'route': ['td_1', 'F_2_1', 'F_2_2', 'F_2_3'], 'route_dis': 38.46198258839964}
					node_dis = item['route_dis'] + dis_to_pre_node
					seat_pre_node_to_four_exit[i] = node_dis

			if next_node !='null':
				#同一排节点
				next_node_label = next_node + '_' + l_arr[1]

				dis_to_next_node = calDistance(coord,dict_node[next_node_label]['coord'])
				# 计算路径
				route = all_node_dis[next_node_label]
				for i in range(len(route)):

					item = route[i]
					# i = {'route': ['td_1', 'F_2_1', 'F_2_2', 'F_2_3'], 'route_dis': 38.46198258839964}
					node_dis = item['route_dis'] + dis_to_next_node
					seat_next_node_to_four_exit[i] = node_dis 

			#分别比较从两边出去的需要的总的时间
			for x in range(4):
				# print('x',x)
				# print(seat_pre_node_to_four_exit)
				# print(seat_next_node_to_four_exit)
				min_dis = min([seat_pre_node_to_four_exit[x],seat_next_node_to_four_exit[x]])
				dis_to_exit.append(min_dis)
				# print('dis_to_exit',dis_to_exit)

		SeatDis[label] = dis_to_exit
		seat_dis_arr.append(dis_to_exit)

	return SeatDis,seat_dis_arr


print(len(getAllSeatDis()))









