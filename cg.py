#coding:utf-8
import os
# import numpy as np
# import pandas as pd


# data = pd.read_excel('point.xlsx','seat')
# 
#读取csv文件
import csv
import matplotlib.pyplot as plt

#出口
EXIT_X = [16420,34720,6565,43875]
EXIT_Y = [30852,6587,18720,18720]

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
        	# plt.text(row[1],row[2],str(row[0]), family='serif', style='italic', ha='right', wrap=True)
        	# print(row[1],row[2])
        	# 
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
        	x_td.append(row[1])
        	y_td.append(row[2])
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
        	x_lt.append(row[1])
        	y_lt.append(row[2])
        	label_lt.append(row[0])
        	# plt.text(row[1],row[2],str(row[0]), family='serif', style='italic', ha='right', wrap=True)
        	# print(row[1],row[2])
##读取辅助点
x_fz = []
y_fz = []
label_fz = []
with open('point_fz.csv', 'rb') as f:        # 采用b的方式处理可以省去很多问题
    reader = csv.reader(f)
    # print(type(reader))
    for row in reader:
        # do something with row, such as row[0],row[1]
        if row[1] != 'x':
        	x_fz.append(row[1])
        	y_fz.append(row[2])
        	label_fz.append(row[0])
        	# plt.text(row[1],row[2],str(row[0]), family='serif', style='italic', ha='right', wrap=True)
        	# print(row[1],row[2])
        	# 
        	
fig = plt.figure(figsize=(80, 56), dpi=50)


plt.plot(x_zw,y_zw,'ro',color='blue',label='xujing')
plt.plot(EXIT_X,EXIT_Y,'ro',color='green',label='xujing')

plt.plot(x_lt,y_lt,'ro',color='red',label='xujing')
plt.plot(x_fz,y_fz,'ro',color='red',label='xujing')

for i in range(len(x_zw)):
	plt.text(x_zw[i],y_zw[i],str((x_zw[i],y_zw[i])))
for i in range(len(x_td)):
	plt.text(x_td[i],y_td[i],str((x_td[i],y_td[i])))
for i in range(len(x_lt)):
	plt.text(x_lt[i],y_lt[i],str((x_lt[i],y_lt[i])))
for i in range(len(x_fz)):
	plt.text(x_fz[i],y_fz[i],str((x_fz[i],y_fz[i])))

# window = fig.add_subplot(111)

# plt.scatter(x_zw, y_zw, s=200, c='blue')
# plt.scatter(x_lt, y_lt, s=200, c='red')
# plt.scatter(x_td, y_td, s=200, c='green')
# plt.scatter(select_right_x, select_right_y, s=20, c='red')
# print(len(select_right_x),len(select_right_y))
# plt.plot(x, y, 'ro')
plt.xlim(0, 50000)
plt.ylim(0, 40000)
plt.xlabel('x 49000')
plt.ylabel('y 35000')
plt.title('evacuation')
plt.grid(True)
plt.savefig('image_init.png')
plt.show()


# import csv
# with open('some.csv', 'wb') as f:      # 采用b的方式处理可以省去很多问题
#     writer = csv.writer(f)
#     writer.writerows(someiterable)