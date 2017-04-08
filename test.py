a = [1, 2, 0, 3, 4, 0, 5, 0, 6]
a = filter(lambda x: x > 0, a)
print a


import matplotlib.pyplot as plt

def draw():
    # plt.plot([1,2,3], [1,2,3], 'go-', label='line 1', linewidth=2)
    plt.plot([1,2,3,2,6], [1,4,9,5,6], 'rv',  label='line 2')
    # plt.axis([0, 4, 0, 10])
    # plt.legend()
    plt.show()

draw()