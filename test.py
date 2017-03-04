# -*- coding:utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

#
#
def plot(x1,y1,x2,y2,x3,y3,sample_size):

    theta = np.arange(0, 1, 0.001)
    x = theta * x1 + (1 - theta) * x2
    y = theta * y1 + (1 - theta) * y2
    plt.plot(x, y, 'g--', linewidth=2)
    x = theta * x1 + (1 - theta) * x3
    y = theta * y1 + (1 - theta) * y3
    plt.plot(x, y, 'g--', linewidth=2)
    x = theta * x2 + (1 - theta) * x3
    y = theta * y2 + (1 - theta) * y3
    plt.plot(x, y, 'g--', linewidth=2)
    rnd1 = np.random.random(size=sample_size)
    rnd2 = np.random.random(size=sample_size)
    rnd3 = np.random.random(size=sample_size)
    rnd2 = np.sqrt(rnd2)
    x = rnd2 * (rnd1 * x1 + (1 - rnd1) * x2) + (1 - rnd2) * x3 + (1 - rnd3) * x3
    y = rnd2 * (rnd1 * y1 + (1 - rnd1) * y2) + (1 - rnd2) * y3 + (1 - rnd3) * y3

    return x,y

def getplot():
    x1, y1 = 0, 0
    x2, y2 = 0, 20
    x3, y3 = 10, 0
    x4, y4 = 10, 20
    x5, y5 = 20, 0
    x6, y6 = 20, 20
    sample_left_size = 150
    sample_right_size = 300

    plot_x,plot_y = plot(x1, y1, x2, y2, x3, y3, sample_left_size)

    print(plot_x,plot_y )

    plt.plot(plot_x, plot_y, 'ro')
    plt.grid(True)
    # plt.savefig('demo.png')
    plt.show()

if __name__ == "__main__" :
    getplot()


# if __name__ == '__main__':

