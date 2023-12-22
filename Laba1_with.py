import numpy as np
import sympy as sp
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def Rot2D(x, y, alpha):
    Rx = x * np.cos(alpha) - y * np.sin(alpha)
    Ry = x * np.sin(alpha) + y * np.cos(alpha)
    return Rx, Ry

T = np.linspace(0, 10, 300)

t = sp.Symbol('t')

r = 2 + 0.5 * sp.sin(12 * t)
phi = 1.2 * t + 0.2 * sp.cos(12 * t)

x = r * sp.cos(phi)
y = r * sp.sin(phi)

X = np.zeros_like(T)
Y = np.zeros_like(T)

VX = np.zeros_like(T)
VY = np.zeros_like(T)

AX = np.zeros_like(T)
AY = np.zeros_like(T)

A = np.zeros_like(T)
AT = np.zeros_like(T)

Curve = np.zeros_like(T)

Vx = sp.diff(x, t)
Vy = sp.diff(x, t)

V = sp.sqrt(Vx ** 2 + Vy ** 2)

VxN = Vx / V
VyN = Vy / V

Ax = sp.diff(Vx, t)
Ay = sp.diff(Vy, t)

A_full = sp.sqrt(Ax ** 2 + Ay ** 2)

AxN = Ax / A_full
AyN = Ay / A_full

A_tan = sp.diff(V, t)
A_nor = sp.sqrt(A_full ** 2 - A_tan ** 2)

R_cur = (V ** 2) / A_nor

AtanX = Vx / V * A_tan
AtanY = Vy / V * A_tan

for i in np.arange(len(T)):
    X[i] = sp.Subs(x, t, T[i])
    Y[i] = sp.Subs(y, t, T[i])

    VX[i] = sp.Subs(VxN, t, T[i])
    VY[i] = sp.Subs(VyN, t, T[i])

    AX[i] = sp.Subs(AxN, t, T[i])
    AY[i] = sp.Subs(AyN, t, T[i])

    Curve[i] = sp.Subs(R_cur, t, T[i])

fig = plt.figure()

ax1 = fig.add_subplot(1, 1, 1)
ax1.axis('equal')
ax1.set(xlim = [-10, 10], ylim = [-10, 10])

ax1.plot(X, Y)

# Точка
P, = ax1.plot(X[0], Y[0], marker = 'o')

# Линии скорости, ускорения, радиус-вектора, радиуса кривизны
VLine, = ax1.plot([X[0], X[0] + VX[0]], [Y[0], Y[0] + VY[0]], 'r')
ALine, = ax1.plot([X[0], X[0] + AX[0]], [Y[0], Y[0] + AY[0]], 'b')
RLine, = ax1.plot([0, X[0]], [0, Y[0]], 'pink')
CurveVec, = ax1.plot([X[0], X[0] + (Y[0] + VY[0]) * Curve[0] / sp.sqrt((Y[0] + VY[0]) ** 2 + (X[0] + VX[0])** 2)], [Y[0], Y[0] - (X[0] + VX[0]) * Curve[0] / sp.sqrt((Y[0] + VY[0]) ** 2 + (X[0] + VX[0]) ** 2)], 'orange')

# Шаблон стрелки
ArrowX = np.array([-0.2, 0, -0.2])
ArrowY = np.array([0.1, 0, -0.1])

# Стрелка скорости
RVArrowX, RVArrowY = Rot2D(ArrowX, ArrowY, math.atan2(VY[0], VX[0]))
VArrow, = ax1.plot(RVArrowX + X[0] + VX[0], RVArrowY + Y[0] + VY[0], 'r')

# Стрелка ускорения
RAArrowX, RAArrowY = Rot2D(ArrowX, ArrowY, math.atan2(AY[0], AX[0]))
AArrow, = ax1.plot(RAArrowX + X[0], RAArrowY + Y[0], 'b') #+AX[0]

# Стрелка радиус-вектора
RRArrowX, RRArrowY = Rot2D(ArrowX, ArrowY, math.atan2(Y[0], X[0]))
RArrow, = ax1.plot(RRArrowX + X[0], RRArrowY + Y[0], 'pink')

def anima(i):
    P.set_data([X[i]], [Y[i]])

    # Скорость
    VLine.set_data([X[i], X[i] + VX[i]], [Y[i], Y[i] + VY[i]])
    RVArrowX, RVArrowY = Rot2D(ArrowX, ArrowY, math.atan2(VY[i], VX[i]))
    VArrow.set_data(RVArrowX + X[i] + VX[i], RVArrowY + Y[i] + VY[i])

    # Ускорение
    ALine.set_data([X[i], X[i] + AX[i]], [Y[i], Y[i] + AY[i]])
    RAArrowX, RAArrowY = Rot2D(ArrowX, ArrowY, math.atan2(AY[i], AX[i]))
    AArrow.set_data(RAArrowX + X[i] + AX[i], RAArrowY + Y[i] + AY[i])

    # Радиус-вектор
    RLine.set_data([0, X[i]], [0, Y[i]])
    RRArrowX, RRArrowY = Rot2D(ArrowX, ArrowY, math.atan2(Y[i], X[i]))
    RArrow.set_data(RRArrowX + X[i], RRArrowY + Y[i])

    #Радиус кривизны
    CurveVec.set_data([X[i], (X[i] + (Y[i] + VY[i]) * Curve[i] / sp.sqrt((Y[i] + VY[i]) ** 2 + (X[i] + VX[i])** 2)) / 10000],
                     [Y[i], (Y[i] - (X[i] + VX[i]) * Curve[i] / sp.sqrt((Y[i] + VY[i]) ** 2 + (X[i] + VX[i]) ** 2)) / 10000])

    return P, VLine, VArrow, ALine, AArrow, RLine, RArrow , CurveVec


anim = FuncAnimation(fig, anima, frames = 1000, interval = 2, repeat = False)

plt.show()


