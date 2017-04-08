# coding:utf-8
import os
import numpy as np
import matplotlib.pyplot as plt
from node import get_node,init_dict_node,calDistance
#读取csv文件
#
import csv
import math

# N*N 数组
#{'link':0,'G':0,'H':0,'F':0,'label':'t_1_2','cood':(121,222)}
# NODE_LINK = [[{'label':'a','link':0,'parent':'start','G':0,'H':0,'F':0},{'label':'b','link':1,'parent':'start','G':2,'H':2,'F':0},{'label':'c','link':1,'parent':'start','G':1,'H':1,'F':0},{'label':'d','link':0,'parent':'start','G':0,'H':3.5,'F':0},{'label':'e','link':0,'parent':'start','G':0,'H':8.5,'F':0}],
#              [{'label':'a','link':1,'parent':'start','G':2,'H':2,'F':0},{'label':'b','link':0,'parent':'start','G':0,'H':0,'F':0},{'label':'c','link':0,'parent':'start','G':0,'H':2.8,'F':0},{'label':'d','link':1,'parent':'start','G':4,'H':4'F':0},{'label':'e','link':0,'parent':'start','G':0,'H':8,'F':0}],
#              [{'label':'a','link':1,'parent':'start','G':1,'H':1,'F':0},{'label':'b','link':1,'parent':'start','G':2,'H':2,'F':0},{'label':'c','link':1,'parent':'start','G':1,'H':1,'F':0},{'label':'d','link':0,'parent':'start','G':0,'H':3.5,'F':0},{'label':'e','link':0,'parent':'start','G':0,'H':8.5,'F':0}],
#              [{'label':'a','link':0,'parent':'start','G':0,'H':0,'F':0},{'label':'b','link':1,'parent':'start','G':2,'H':2,'F':0},{'label':'c','link':1,'parent':'start','G':1,'H':1,'F':0},{'label':'d','link':0,'parent':'start','G':0,'H':3.5,'F':0},{'label':'e','link':0,'parent':'start','G':0,'H':8.5,'F':0}],
#              [{'label':'a','link':0,'parent':'start','G':0,'H':0,'F':0},{'label':'b','link':1,'parent':'start','G':2,'H':2,'F':0},{'label':'c','link':1,'parent':'start','G':1,'H':1,'F':0},{'label':'d','link':0,'parent':'start','G':0,'H':3.5,'F':0},{'label':'e','link':0,'parent':'start','G':0,'H':8.5,'F':0}]]
# #节点中的实际距离
NODE_LINK = init_dict_node()
#标签转成维度id
dict_node = get_node() # {'t_1_1':{'coord':(12,22),'id':0},'t_1_2':{'coord':(5,12),'id':1},'t_1_3':{'coord':(6,8),'id':2},'t_1_4':{'coord':(1,12),'id':3},'t_1_5':{'coord':(1,18),'id':4},'F_1_1':{'coord':(15,12),'id':5},'F_1_2':{'coord':(15,22),'id':6}}

parent_node = {}
NODE_DISTANCE_G = [[0,0,12],
                      [22,0,21]]
# 节点中得欧式距离
NODE_DISTANCE_H = [[0,0,12],
                 [22,0,21]]

NODE_DISTANCE_F = [[0,0,12],
                     [22,0,21]]
#已近访问的节点
visited = []


startNode = (121,22)
targetNode = (12,222)
start_node_id = 0
target_node_id = 50


LAMBDAH = 2.0

# for key in labelToId:
# 	# print(key,labelToId[key])
# 	openList = []
# 	closedList =[]
# 	route = []
# 	cur_node_id = labelToId[key] 
# 	node_link_arr = NODE_LINK_DISTANCE[cur_node_id]
# 	# 存储连接的节点ID
# 	node_link = {}
# 	# node_link_value = []
# 	for item in node_link_arr:
# 		# print(item)
# 		if item != 0:
# 			link_node_id = node_link_arr.index(item)
# 			node_link.append()
# 			link_node_f = f(cur_node_id,link_node_id,target_node_id)
# 			node_link_value[link_node_id] = link_node_f

# 	node_link_sorted = sorted(node_link.items(), key=lambda x: x[1])

# 	move_node = node_link_sorted[0]
# 	move_node_id = move_node[0]


# 	# if len(node_link) == 0:
# 		# pass
# 		# TODO 
	
# 	f = f(cur_node_id,link_node_id,target_node_id)

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


def astar(start_node_label,target_node_label):
	start_node_id = dict_node[start_node_label]['id']
	target_node_id = dict_node[target_node_label]['id']
	openList = []
	closedList =[]
	route = []
	cur_node_id = start_node_id
	print('start_node_id',start_node_id)
	print('target_node_id',target_node_id)
	NODE_LINK[start_node_id][start_node_id]['parent'] = 'startNode'
	openList.append(start_node_id)
	found = False  
	resign = False 
	count = 0

	while not found and not resign:

		# print('next step openList:',openList,'closedList:',closedList)

		node_link_value = {}
		if cur_node_id == target_node_id:
			
			print('========================================fuck! I found it=============================================')
			
			found = True
			route = getRoute(start_node_id,target_node_id)
			# print('route',route)
			break

		# print('cur_node_id node index',openList.index(cur_node_id))
		#从开启列表移除当前节点
		del openList[openList.index(cur_node_id)]
		#当前节点添加到关闭列表
		closedList.append(cur_node_id)

		#如果某个相邻格已经在开启列表里了，检查现在的这条路径是否更好。
		for neighbor in get_neighbors_id(cur_node_id):
			print('neighbor:',neighbor)
			if neighbor not in closedList:

				G_cur_to_neighbor = get_G(cur_node_id,neighbor)
				G_cur_parent = get_P_G(start_node_id,cur_node_id)
				H_neighbor = get_H(neighbor,target_node_id)

				if neighbor in openList:
					print('in openList')
					#换句话说，检查如果我们用新的路径到达它的话，G值是否会更低一些。如果不是，那就什么都不做
					
					
					G_neighbor = get_P_G(start_node_id,neighbor)

					if G_cur_to_neighbor + G_cur_parent < G_neighbor:	                        

						parent_node[neighbor] = cur_node_id
						NODE_LINK[start_node_id][neighbor]['parent'] = cur_node_id

						NODE_LINK[start_node_id][neighbor]['G'] = G_cur_to_neighbor + G_cur_parent
						NODE_LINK[start_node_id][neighbor]['H'] = H_neighbor
						NODE_LINK[start_node_id][neighbor]['F'] = NODE_LINK[start_node_id][neighbor]['G']+ NODE_LINK[start_node_id][neighbor]['H']

						# print('get_F',NODE_LINK[start_node_id][neighbor]['F'])
						node_link_value[neighbor] = NODE_LINK[start_node_id][neighbor]['F']
					else:
						#选择当前节点

						pass
				else:
					print('not in openList')
					parent_node[neighbor] = cur_node_id

					NODE_LINK[start_node_id][neighbor]['parent'] = cur_node_id

					NODE_LINK[start_node_id][neighbor]['G'] = G_cur_to_neighbor + G_cur_parent
					NODE_LINK[start_node_id][neighbor]['H'] = H_neighbor
					NODE_LINK[start_node_id][neighbor]['F'] = NODE_LINK[start_node_id][neighbor]['G']+ NODE_LINK[start_node_id][neighbor]['H']

					# print('get_F',NODE_LINK[start_node_id][neighbor]['F'])

					node_link_value[neighbor] = NODE_LINK[start_node_id][neighbor]['F']
				
					openList.append(neighbor)

			# print('openList',openList)
		# print('node_link_value:',node_link_value)
		#按照得分排序
		node_link_sorted = sorted(node_link_value.items(), key=lambda x: x[1])
		#选择分数最小的
		
		move_node = node_link_sorted[0]
		# print('move_node',move_node)
		#获取id
		cur_node_id = move_node[0]
		print('cur_node_id',cur_node_id)
	return route


def get_neighbors_id(cur_node_id):
	node_link =[]
	node_link_arr = NODE_LINK[cur_node_id]
	#找到与当前节点连接的节点
	for item in node_link_arr:
		# print(item)
		if item['link']!= 0:
			next_node_id = node_link_arr.index(item)
			node_link.append(next_node_id)
	# print('cur_node_id:',cur_node_id,'neighbors_id:',node_link)
	return node_link


#当前节点周围某一个节点到最初节点的实际距离
def get_P_G(start_node_id,link_node_id):

	# print('get_P_G',NODE_LINK[start_node_id][link_node_id]['G'])
	return NODE_LINK[start_node_id][link_node_id]['G']

#当前节点和周围某一个节点的实际距离
def get_G(cur_node_id,link_node_id):
	# global start_node_id
	# print('get_G',NODE_LINK[cur_node_id][link_node_id]['G'])

	return NODE_LINK[cur_node_id][link_node_id]['G']
#估计距离  欧式距离
def get_H(cur_node_id,target_node_id):
	# global start_node_id
	# TODO 要提前计算两点距离
	dict_node_by_id = sorted(dict_node.items(), key=lambda x: x[1]['id'])
	cur_node_coord = dict_node_by_id[cur_node_id][1]['coord']
	target_node_coord = dict_node_by_id[target_node_id][1]['coord']
	# ,cur_node_id,target_node_id,
	# print('get_H',calDistance(cur_node_coord,target_node_coord))
	return calDistance(cur_node_coord,target_node_coord)
	# return NODE_LINK[cur_node_id][target_node_id]['H']

def get_F(cur_node_id,link_node_id):
	global target_node_id
	return get_G(cur_node_id,link_node_id)+get_H(cur_node_id,target_node_id)




def getRouteLabel(start_node_id,route):
	dict_node_by_id = sorted(dict_node.items(), key=lambda x: x[1]['id'])
	routeLabel = []
	# print('start_node_id',start_node_id,'route:',route)
	for i in route:
		# print('NODE_LINK',NODE_LINK[start_node_id][i])

		label = dict_node_by_id[i][0]
		routeLabel.append(label)
	return routeLabel


def getRoute(start_node_id,target_node_id):
	# closedList
	# for i in closedList:
	# print(start_node_id,target_node_id)
	# print('parent_node',parent_node)

	found_route = False
	route_node_id = target_node_id

	route = [target_node_id]
	route_dis = NODE_LINK[start_node_id][target_node_id]['G']
	# print('NODE_LINK_getRoute',NODE_LINK[start_node_id])
	while not found_route:
		
		route_node_id = parent_node[route_node_id]

		

		route.append(route_node_id)

		if int(start_node_id) == int(route_node_id):
			# print('fuck')
			found_route = True


	# print('getRoute',,'dis',route_dis)

	resRoute = {'route':getRouteLabel(start_node_id,route),'route_dis':route_dis}
	return resRoute 
	# NODE_LINK[]



# print(np.shape(np.array(init_dict_node())))

# print(np.shape(np.array(init_dict_node())[:,1]))
# print(np.array(init_dict_node())[:,0])
# print(init_dict_node())
# def aStar(startNode,targetNode,NODE_LINK,NODE_LINK_DISTANCE):
def getAllNodeDis():
	dict_node_by_id = sorted(dict_node.items(), key=lambda x: x[1]['id'])
	AllNodeDisArr = []
	AllNodeDis = {}
	for i in range(len(dict_node_by_id)-4):
	# for item in  dict_node_by_id:
		
		lable = dict_node_by_id[i][0]
		dis = []
		for td in ['td_1','td_2','td_3','td_4']:
			dis_td = astar(lable,td)
			print('lable',lable,'td',td,'aStar',dis_td)
			dis.append(dis_td)

		AllNodeDis[lable] = dis
		AllNodeDisArr.append(dis)
	print('AllNodeDis',AllNodeDis)
	print('AllNodeDis',len(AllNodeDis),np.shape(AllNodeDisArr))

#得到所有节点到四个出口的最短路径
getAllNodeDis()






# print()
# dict_node_by_id = sorted(dict_node.items(), key=lambda x: x[1]['id'])
# cur_node_coord = dict_node_by_id[1][1]['coord']
# target_node_coord = dict_node_by_id[65][1]['coord']

# print(cur_node_coord,target_node_coord)





