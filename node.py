#coding:utf-8
import os
import numpy as np
# import pandas as pd


# data = pd.read_excel('point.xlsx','seat')
# 
#读取csv文件
# 1，把起始格添加到开启列表。
# 2，重复如下的工作：
#   a) 寻找开启列表中F值最低的格子。我们称它为当前格。
#   b) 把它切换到关闭列表。
#   c) 对相邻的格中的每一个？
#       * 如果它不可通过或者已经在关闭列表中，略过它。反之如下。
#       * 如果它不在开启列表中，把它添加进去。把当前格作为这一格的父节点。记录这一格的F,G,和H值。
#       * 如果它已经在开启列表中，用G值为参考检查新的路径是否更好。更低的G值意味着更好的路径。
#       如果是这样，就把这一格的父节点改成当前格，并且重新计算这一格的G和F值。
#       如果你保持你的开启列表按F值排序，改变之后你可能需要重新对开启列表排序。
#   d) 停止，当你
#       * 把目标格添加进了关闭列表(注解)，这时候路径被找到，或者
#       * 没有找到目标格，开启列表已经空了。这时候，路径不存在。
# 3.保存路径。从目标格开始，沿着每一格的父节点移动直到回到起始格。这就是你的路径。
import csv
# import matplotlib.pyplot as plt


ROW_NODE_LINK = ['t_1','F_1','t_2','t_3','null','t_4','t_5','null','t_6','F_2','t_7','t_8','t_9','null','t_10','t_11','null']
NODE_LINK_SHOW =[]
# EXIT_NODE_LINK = 
dict_node = {}
# {'t_1_1':{'coord':(12,22),'id':0},'t_1_2':{'coord':(5,12),'id':1},'t_1_3':{'coord':(6,8),'id':2},'t_1_4':{'coord':(1,12),'id':3},'t_1_5':{'coord':(1,18),'id':4},'F_1_1':{'coord':(15,12),'id':5},'F_1_2':{'coord':(15,22),'id':6}}

def get_node():
	node = {}
	with open('point_node.csv', 'rb') as f:        # 采用b的方式处理可以省去很多问题
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


	            
	           	


def calDistance(cur_node, link_node):
	# print(cur_node, link_node)
	x1 = float(cur_node[0])
	y1 = float(cur_node[1])
	x2 = float(link_node[0])
	y2 = float(link_node[1])
	return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

def getNear(label):
	# print('input_label',label)
	node = dict_node[label]
	
	coord = node['coord']
	node_id = node['id']
	nearNode = []
	arr = label.split('_')

	# print(arr[2])
	if int(arr[2]) == 1:
		next_node = arr[0]+'_'+arr[1]+'_'+str(int(arr[2])+1)
		nearNode.append(next_node)
		#第一排的节点都可以和四个门相连
		nearNode.append('td_1')
		nearNode.append('td_2')
		nearNode.append('td_3')
		nearNode.append('td_4')



	elif int(arr[2]) < 5 and int(arr[2]) > 1:

		# print(arr[2])
		next_node = arr[0]+'_'+arr[1]+'_'+str(int(arr[2])-1)
		nearNode.append(next_node)

		next_node = arr[0]+'_'+arr[1]+'_'+str(int(arr[2])+1)
		nearNode.append(next_node)
	elif int(arr[2]) == 5:
		next_node = arr[0]+'_'+arr[1]+'_'+str(int(arr[2])-1)
		nearNode.append(next_node)


	node_index = ROW_NODE_LINK.index(arr[0]+'_'+arr[1])

	# print('node_index',node_index)
	next_node_row = ROW_NODE_LINK[node_index+1]
	# print('next_node_row',next_node_row)
	if next_node_row != 'null':

		next_node = next_node_row+'_'+arr[2]
		nearNode.append(next_node)

	if node_index > 0:
		next_node_row = ROW_NODE_LINK[node_index-1]
		if next_node_row != 'null':
			next_node = next_node_row+'_'+arr[2]
			nearNode.append(next_node)

	# print('ouput_label',label,'nearNode',nearNode)
	return nearNode

# print(getNear('t_1_2'))
# dict_node_TEST = {'t_1_1':{'coord':(12,22),'id':0},'t_1_2':{'coord':(12,22),'id':0}}



def init_dict_node():

	global dict_node
	dict_node = get_node()	

	# print('dict_node',len(dict_node))
	# print('dict_node',dict_node)
	NODE_LINK = []

	dict_node_arr = sorted(dict_node.items(), key=lambda x: x[1]['id'])




	for i in range(len(dict_node_arr)-4):
		key = dict_node_arr[i][0]

	
		node_arr = [{'label':'','link':0,'parent':'','G':0,'H':0,'F':0} for i in range(len(dict_node))]
		node_arr_show = [0 for i in range(len(dict_node))]

		label = key 
		cur_coord = dict_node[key]['coord']
		cur_id = dict_node[key]['id']

		for item in getNear(label):
			collect = {}
			# print('item',item)
			next_node_coord = dict_node[item]['coord']
			next_node_id = dict_node[item]['id']
			distance = calDistance(cur_coord,next_node_coord)
			
			collect['label'] = item
			collect['link'] = 1
			collect['parent'] = ''
			collect['G'] = distance
			collect['H'] = None
			collect['F'] = None 

			node_arr[next_node_id] = collect
			node_arr_show[next_node_id] = 1
			# NODE_LINK[cur_id][next_node_id] = collect
		

		NODE_LINK.append(node_arr)
		NODE_LINK_SHOW.append(node_arr_show)
	print('NODE_LINK_SHOW')
	# print(NODE_LINK_SHOW)
	return NODE_LINK




# [('t_1_1', {'id': 0, 'coord': (6.565, 10.142)}), ('t_1_2', {'id': 1, 'coord': (5.564, 9.727)}), ('t_1_3', {'id': 2, 'coord': (4.666, 9.355)}), ('t_1_4', {'id': 3, 'coord': (3.765, 8.982)}), ('t_1_5', {'id': 4, 'coord': (2.865, 8.609)}), ('F_1_1', {'id': 5, 'coord': (9.548, 6.589)}), ('F_1_2', {'id': 6, 'coord': (9.129, 5.587)}), ('F_1_3', {'id': 7, 'coord': (8.756, 4.687)}), ('F_1_4', {'id': 8, 'coord': (8.384, 3.787)}), ('F_1_5', {'id': 9, 'coord': (8.011, 2.887)}), ('t_2_1', {'id': 10, 'coord': (15.22, 6.587)}), ('t_2_2', {'id': 11, 'coord': (15.22, 5.579)}), ('t_2_3', {'id': 12, 'coord': (15.22, 4.687)}), ('t_2_4', {'id': 13, 'coord': (15.22, 3.787)}), ('t_2_5', {'id': 14, 'coord': (15.22, 2.887)}), ('t_3_1', {'id': 15, 'coord': (32.47, 6.587)}), ('t_3_2', {'id': 16, 'coord': (32.47, 5.579)}), ('t_3_3', {'id': 17, 'coord': (32.47, 4.687)}), ('t_3_4', {'id': 18, 'coord': (32.47, 3.787)}), ('t_3_5', {'id': 19, 'coord': (32.47, 2.887)}), ('t_4_1', {'id': 20, 'coord': (40.298, 6.591)}), ('t_4_2', {'id': 21, 'coord': (40.713, 5.591)}), ('t_4_3', {'id': 22, 'coord': (41.085, 4.691)}), ('t_4_4', {'id': 23, 'coord': (41.458, 3.791)}), ('t_4_5', {'id': 24, 'coord': (41.831, 2.891)}), ('t_5_1', {'id': 25, 'coord': (43.875, 10.142)}), ('t_5_2', {'id': 26, 'coord': (44.87, 9.727)}), ('t_5_3', {'id': 27, 'coord': (45.77, 9.355)}), ('t_5_4', {'id': 28, 'coord': (46.67, 8.972)}), ('t_5_5', {'id': 29, 'coord': (47.57, 8.609)}), ('t_6_1', {'id': 30, 'coord': (43.875, 27.298)}), ('t_6_2', {'id': 31, 'coord': (44.87, 27.712)}), ('t_6_3', {'id': 32, 'coord': (45.77, 28.085)}), ('t_6_4', {'id': 33, 'coord': (46.67, 28.458)}), ('t_6_5', {'id': 34, 'coord': (47.57, 28.831)}), ('F_2_1', {'id': 35, 'coord': (40.893, 30.852)}), ('F_2_2', {'id': 36, 'coord': (41.328, 31.895)}), ('F_2_3', {'id': 37, 'coord': (41.681, 32.748)}), ('F_2_4', {'id': 38, 'coord': (42.065, 33.675)}), ('F_2_5', {'id': 39, 'coord': (42.434, 34.565)}), ('t_7_1', {'id': 40, 'coord': (33.97, 30.842)}), ('t_7_2', {'id': 41, 'coord': (33.97, 31.747)}), ('t_7_3', {'id': 42, 'coord': (33.97, 32.747)}), ('t_7_4', {'id': 43, 'coord': (33.97, 33.747)}), ('t_7_5', {'id': 44, 'coord': (33.97, 34.747)}), ('t_8_1', {'id': 45, 'coord': (32.66, 31.568)}), ('t_8_2', {'id': 46, 'coord': (32.66, 33.058)}), ('t_8_3', {'id': 47, 'coord': (32.66, 34.56)}), ('t_9_1', {'id': 48, 'coord': (17.78, 31.568)}), ('t_9_2', {'id': 49, 'coord': (17.78, 33.058)}), ('t_10_1', {'id': 50, 'coord': (10.142, 30.852)}), ('t_10_2', {'id': 51, 'coord': (9.727, 31.745)}), ('t_10_3', {'id': 52, 'coord': (9.355, 32.638)}), ('t_10_4', {'id': 53, 'coord': (8.982, 33.531)}), ('t_10_5', {'id': 54, 'coord': (8.609, 34.424)}), ('t_11_1', {'id': 55, 'coord': (6.57, 27.298)}), ('t_11_2', {'id': 56, 'coord': (5.565, 27.712)}), ('t_11_3', {'id': 57, 'coord': (4.56, 28.085)}), ('t_11_4', {'id': 58, 'coord': (3.555, 28.458)}), ('t_11_5', {'id': 59, 'coord': (2.55, 28.831)}), ('td_1', {'id': 60, 'coord': (6.565, 18.72)}), ('td_2', {'id': 61, 'coord': (34.72, 6.587)}), ('td_3', {'id': 62, 'coord': (43.875, 18.72)}), ('td_4', {'id': 63, 'coord': (16.42, 30.852)})]


