import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import math
from scipy.integrate import odeint

t_fin = 10
t = np.linspace(0, t_fin, 1000)

m1 = 200
m2 = 5
r = 0.4
g = 9.81

def odesys(y, t, m1, m2, r, g):
    dy = np.zeros(4)
    dy[0] = y[2]
    dy[1] = y[3]

    a11 = m1 + m2
    a12 = m2 * r * np.cos(y[1])
    a21 = np.cos(y[1])
    a22 = r

    b1 = m2 * r * np.sin(y[1]) * (y[3] ** 2)
    b2 = -g * np.sin(y[1])

    dy[2] = (b1 * a22 - b2 * a12) / (a11 * a22 - a12 * a21)
    dy[3] = (b2 * a11 - b1 * a21) / (a11 * a22 - a12 * a21)

    return dy

s0 = 0
phi0 = 0
ds0 = 0
dphi0 = 0

y0 = [s0, phi0, ds0, dphi0]

Y = odeint(odesys, y0, t, (m1, m2, r, g))

s = Y[:, 0]
phi = Y[:, 1]
ds = Y[:,2]
dphi = Y[:,3]

dds = [odesys(y0, t, m1, m2, r, g)[2] for y, t in zip(Y, t)]
ddphi = [odesys(y0, t, m1, m2, r, g)[3] for y, t in zip(Y, t)]

R_2 = (m1 + m2) * g + m2 * r * (ddphi * np.sin(phi) + dphi ** 2 * np.cos(phi))
N = m2 * (g * np.cos(phi) - dds * np.sin(phi) + r * dphi ** 2)

O = s

XA = 2.5 + s
YA = 1.5

XB = XA + r * np.sin(phi)
YB = YA - r * np.cos(phi)

Xtr = np.array([1, 1.5, 3.5, 4, 1])
Ytr = np.array([0, 3, 3, 0, 0])

fig = plt.figure(figsize= [1, 1])
ax = fig.add_subplot(1, 2, 1)
ax.set(xlim = [-2, 10], ylim = [-1, 5])
ax.set_aspect('equal')

X_Ground = [-1, -1, 9]
Y_Ground = [4, 0, 0]

ax.plot(X_Ground, Y_Ground, color = 'Black')

Trap = ax.plot(O[0] + Xtr, Ytr)[0]
Rad = ax.plot([XA[0], XB[0]], [YA, YB[0]])[0]
Point_A = ax.plot(XA[0], YA, marker = 'o')[0]

#Вторая точка
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

ax_for_graphs = fig.add_subplot(2, 2, 4)
ax_for_graphs.set_title("s(t)")
ax_for_graphs.plot(t, s)
ax_for_graphs.grid(True)

ax_for_graphs = fig.add_subplot(2, 2, 2)
ax_for_graphs.set_title("phi(t)")
ax_for_graphs.plot(t, phi)
ax_for_graphs.grid(True)

fig_for_graphs = plt.figure(figsize = [13, 7])
ax2 = fig_for_graphs.add_subplot(2, 2, 1)
ax2.set_title("N(t)")
ax2.plot(t, N)
ax2.grid(True)

ax2 = fig_for_graphs.add_subplot(2, 2, 3)
ax2.set_title("R(t)")
ax2.plot(t, R_2)
ax2.grid(True)

ax2 = fig_for_graphs.add_subplot(2, 2, 2)
ax2.set_title("dds(t)")
ax2.plot(t, dds)
ax2.grid(True)

ax2 = fig_for_graphs.add_subplot(2, 2, 4)
ax2.set_title("ddphi(t)")
ax2.plot(t, ddphi)
ax2.grid(True)

def anima(i):
    Point_A.set_data(XA[i], YA)
    Rad.set_data([XA[i], XB[i]], [YA, YB[i]])
    Trap.set_data(O[i] + Xtr, Ytr)

    Point_B.set_data(XB[i] + R * np.cos(angles), YB[i] + R * np.sin(angles))

    Drawed_Circle.set_data(XA[i] + X_Circle, YA + Y_Circle)
    Drawed_Circle2.set_data(XA[i] + X_Circle2, YA + Y_Circle2)

    return Point_A, Rad, Point_B, Trap, Drawed_Circle, Drawed_Circle2

anim = FuncAnimation(fig, anima, frames = 1000, interval = 0.01, blit = True)

plt.show()