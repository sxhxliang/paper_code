# coding:utf-8
import os
import numpy as np
import matplotlib.pyplot as plt

#读取csv文件
#
import csv
import math

# N*N 数组
NODE_LINK = [[0,0,1],
             [1,0,1]]

#节点中的实际距离
NODE_DISTANCE_G = [[0,0,12],
                      [22,0,21]]
# 节点中得欧式距离
NODE_DISTANCE_H = [[0,0,12],
                 [22,0,21]]

NODE_DISTANCE_F = [[0,0,12],
                     [22,0,21]]
#已近访问的节点
visited = []
#标签转成维度id
labelToId = {'t_1_1':0,'t_1_2':1}

startNode = (121,22)
targetNode = (12,222)
target_node_id = 50


LAMBDAH = 2.0

for key in labelToId:
	# print(key,labelToId[key])
	openList = []
	closedList =[]
	route = []
	cus_node_id = labelToId[key] 
	node_link_arr = NODE_LINK_DISTANCE[cus_node_id]
	# 存储连接的节点ID
	node_link = {}
	# node_link_value = []
	for item in node_link_arr:
		# print(item)
		if item != 0:
			link_node_id = node_link_arr.index(item)
			node_link.append()
			link_node_f = f(cus_node_id,link_node_id,target_node_id)
			node_link_value[link_node_id] = link_node_f

	node_link_sorted = sorted(node_link.items(), key=lambda x: x[1])

	move_node = node_link_sorted[0]
	move_node_id = move_node[0]


	# if len(node_link) == 0:
		# pass
		# TODO 
	
	f = f(cus_node_id,link_node_id,target_node_id)

# a) 寻找开启列表中F值最低的格子。我们称它为当前格。

# b) 把它切换到关闭列表。

# c) 对相邻的格中的每一个？

#   * 如果它不可通过或者已经在关闭列表中，略过它。反之如下。

#   * 如果它不在开启列表中，把它添加进去。把当前格作为这一格的父节点。记录这一格的F,G,和H值。

#   * 如果它已经在开启列表中，用G值为参考检查新的路径是否更好。更低的G值意味着更好的路径。如果是这样，就把这一格的父节点改成当前格，并且重新计算这一格的G和F值。如果你保持你的开启列表按F值排序，改变之后你可能需要重新对开启列表排序。

# d) 停止，当你

#   * 把目标格添加进了关闭列表(注解)，这时候路径被找到，或者

#   * 没有找到目标格，开启列表已经空了。这时候，路径不存在。
#   

def astar():
	start_node_id = 2
	target_node_id = 50
	openList = []
	closedList =[]
	route = []
	cur_node_id = start_node_id

	openList.append(start_node_id)
	found = False  
    resign = False 
    count = 0
    
    while not found and not resign:

		node_link_value = {}
		if cur_node_id == target_node_id:
			return route
		
		#从开启列表移除当前节点
		openList.remove(openList.index(cur_node_id))
		#当前节点添加到关闭列表
		closedList.append(cur_node_id)

		#如果某个相邻格已经在开启列表里了，检查现在的这条路径是否更好。
		for neighbor in get_neighbors(cur_node_id):
			if neighbor not in closed_list:
				if node in openList:
					#换句话说，检查如果我们用新的路径到达它的话，G值是否会更低一些。如果不是，那就什么都不做
					if get_G(neighbor,cus_node_id) + get_G(cur_node_id) < get_G(neighbor):
	                        
	                        new_map[y][x].parent = cur_node
	                        new_map[y][x].G = get_G(neighbor,cur_node) + get_G(cur_node)
	                        new_map[y][x].H = get_H(neighbor,target_node)
	                        new_map[y][x].F = new_map[y][x].G + new_map[y][x].H
	                    else:
	                        pass
				else:



				
		#按照得分排序
		node_link_sorted = sorted(node_link.items(), key=lambda x: x[1])
		#选择分数最小的
		move_node = node_link_sorted[0]
		#获取id
		move_node_id = move_node[0]
		#把当前id 放入closedList
		
		if move_node_id not in closedList
		
		
		#查看分值最小的id 在不在openlist中
		
		#
		#把当前所有周围的节点放入open中
		#
		
		#
		#
		#
		#
		#


def get_neighbors(cus_node_id):
	node_link =[]
	node_link_arr = NODE_DISTANCE_G[cus_node_id]
	#找到与当前节点连接的节点
	for item in node_link_arr:
		# print(item)
		if item != 0:
			link_node_id = node_link_arr.index(item)
			node_link.append(link_node_id)
			link_node_f = get_F(cus_node_id,link_node_id,target_node_id)
			NODE_DISTANCE_F[cus_node_id][link_node_id] = link_node_f
	return node_link





def get_G(cus_node_id,link_node_id):
	return NODE_DISTANCE_G[cus_node_id][link_node_id]

def get_H(cus_node_id,target_node_id):
	return NODE_DISTANCE_H[cus_node_id][target_node_id]

def get_F(cus_node_id,link_node_id,target_node_id):
	return get_G(cus_node_id,link_node_id)+LAMBDAH*get_H(cus_node_id,target_node_id)










# def aStar(startNode,targetNode,NODE_LINK,NODE_LINK_DISTANCE):







