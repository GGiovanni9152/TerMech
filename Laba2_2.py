import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import math

t_fin = 10
t = np.linspace(0, t_fin, 1000)

#Параметры системы
s = np.cos(3 * t)
phi = 4 * np.sin(t - 10)
r = 0.4
R = 0.1

O = s

#Центр трапеции
XA = 2.5 + s
YA = 1.5

#Центр шарика
XB = XA + r * np.sin(phi)
YB = YA - r * np.cos(phi)

#Создание трапеции
Xtr = np.array([1, 1.5, 3.5, 4, 1])
Ytr = np.array([0, 3, 3, 0, 0])

#Создание графика
fig = plt.figure(figsize= [1, 1])
ax = fig.add_subplot(1, 2, 1)
ax.set(xlim = [-2, 10], ylim = [-1, 5])
ax.set_aspect('equal')

#Опоры
X_Ground = [-1, -1, 9]
Y_Ground = [4, 0, 0]

ax.plot(X_Ground, Y_Ground, color = 'Black')

#Отрисовка трапеции
Trap = ax.plot(O[0] + Xtr, Ytr)[0]
Rad = ax.plot([XA[0], XB[0]], [YA, YB[0]])[0]
Point_A = ax.plot(XA[0], YA, marker = 'o')[0]

#Шарик
angles = np.linspace(0, 2 * math.pi, 1000)
R = 0.1
Point_B = ax.plot(XB[0] + R * np.cos(angles), YB[0] + R * np.sin(angles))[0]

#Маленькая окружность
X_Circle = (r - R) * np.cos(angles)
Y_Circle = (r - R) * np.sin(angles)
Drawed_Circle = ax.plot(XA[0] + X_Circle, YA + Y_Circle, 'green')[0]

#Большая окружность
X_Circle2 = (R + r) * np.cos(angles)
Y_Circle2 = (R + r) * np.sin(angles)
Drawed_Circle2 = ax.plot(XA[0] + X_Circle2, YA + Y_Circle2, 'green')[0]


def anima(i):
    Point_A.set_data(XA[i], YA)
    Point_B.set_data(XB[i] + R * np.cos(angles), YB[i] + R * np.sin(angles))

    Rad.set_data([XA[i], XB[i]], [YA, YB[i]])
    Trap.set_data(O[i] + Xtr, Ytr)

    Drawed_Circle.set_data(XA[i] + X_Circle, YA + Y_Circle)
    Drawed_Circle2.set_data(XA[i] + X_Circle2, YA + Y_Circle2)

    return Point_A, Point_B, Rad, Trap, Drawed_Circle, Drawed_Circle2

anim = FuncAnimation(fig, anima, frames = 1000, interval = 0.01, blit = True)

plt.show()