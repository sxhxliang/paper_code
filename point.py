import numpy as np
import matplotlib.pyplot as plt
select_left_x = []
select_left_y = []

select_right_x = []
select_right_y = []

for xi in range(20):
    x = xi*0.5+0.25

    for yi in range(40):
        y = yi*0.5+0.25
        select_left_x.append(x)
        select_left_y.append(y)

for xi in range(20):
    x = xi*0.5+10.25

    for yi in range(40):
        y = yi*0.5+0.25
        select_right_x.append(x)
        select_right_y.append(y)

print(len(select_left_x))
print(len(select_left_y))
print(len(select_right_x))
print(len(select_right_y))

for d in range(500):
    # print(d)
    # num = 799 - d
    xi = np.random.randint(0, 799)
    select_left_x[xi] = None
    select_left_y[xi] = None

for d in range(200):
    # num = 799 - d
    xi = np.random.randint(0, 799)
    select_right_x[xi] = None
    select_right_y[xi] = None

print(len(select_left_x))
fig = plt.figure(figsize=(20, 20), dpi=50)
# window = fig.add_subplot(111)
plt.scatter(select_left_x, select_left_y, s=20, c='blue')
plt.scatter(select_right_x, select_right_y, s=20, c='red')
# print(len(select_right_x),len(select_right_y))
# plt.plot(select_left_x, select_left_y, 'ro')
plt.xlim(0, 20)
plt.ylim(0, 20)
plt.xlabel('x 20m')
plt.ylabel('y 20m')
plt.title('evacuation')
plt.grid(True)
plt.savefig('imag.png')
plt.show()