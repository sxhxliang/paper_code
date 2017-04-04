import matplotlib.pyplot as plt
from numpy.random import rand
import numpy
import os
import cv2

#setting plt
plt.xlim(xmax=100,xmin=0)
plt.ylim(ymax=100,ymin=0)
plt.xlabel("height")
plt.ylabel("width")


path_1 = r'D:\zhangjichao\view\V7_scale_2\path_1'


x = []
y = []
files = os.listdir(path_1)
for f in files:
    img = cv2.imread(path_1 + '\\' + f)
    x.append(img.shape[0])
    y.append(img.shape[1])
plt.plot(x,y,'ro',color='red',label='path_1')

path_2 = r'D:\zhangjichao\view\V7_scale_2\path_2'

x = []
y = []
files = os.listdir(path_2)
for f in files:
    img = cv2.imread(path_2 + '\\' + f)
    x.append(img.shape[0])
    y.append(img.shape[1])
plt.plot(x,y,'ro',color='red',label='path_2')

path_3 = r'D:\zhangjichao\view\V7_scale_2\path_3'


x = []
y = []
files = os.listdir(path_3)
for f in files:
    img = cv2.imread(path_3 + '\\' + f)
    x.append(img.shape[0])
    y.append(img.shape[1])
plt.plot(x,y,'ro',color='red',label='path_3')

path_4 = r'D:\zhangjichao\view\V7_scale_2\path_4'

x = []
y = []
files = os.listdir(path_4)
for f in files:
    img = cv2.imread(path_4 + '\\' + f)
    x.append(img.shape[0])
    y.append(img.shape[1])
plt.plot(x,y,'ro',color='red',label='path_4')

yujing = r'D:\zhangjichao\view\V7_scale_2\xujing_org_scale_2'

x = []
y = []
files = os.listdir(yujing)
for f in files:
    img = cv2.imread(yujing + '\\' + f)
    x.append(img.shape[0])
    y.append(img.shape[1])
plt.plot(x,y,'ro',color='green' , label='xujing')
for i in range(1,len(x)):
    plt.text(x[i],y[i],str((x[i],y[i])), family='serif', style='italic', ha='right', wrap=True)

plt.legend(loc='upper center', shadow=True, fontsize='x-large')
plt.grid(True)


plt.show()