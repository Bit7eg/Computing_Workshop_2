from matplotlib import pyplot
import numpy as np

import constructor.functions as spline


def get_xi(min_x, max_x, n, i):
    return min_x + i * (max_x - min_x)/n


def f(x):
    return (np.sin(x)**3)*(x*x) + np.cos(x)*x + np.exp(x)


# spline settings
n = 20
a = 3
b = -2
x_min = -20
x_max = 5
eps = 0.00001

# plot settings
left_coord = -24
right_coord = 6
bottom_coord = -450
top_coord = 600
density = 6000

if __name__ == '__main__':
    pyplot.axis([left_coord, right_coord, bottom_coord, top_coord])
    # создание интерполяционной сетки
    x = [get_xi(x_min, x_max, n, i) for i in range(n+1)]
    yf = [f(i) for i in x]
    pyplot.scatter(x, yf, s=10, alpha=1, c='r')
    s = spline.create(x, yf, n, a, b)
    # рисование графика
    x = [left_coord + i * (right_coord - left_coord)/(density - 1) for i in range(density)]
    yf = [f(i) for i in x]
    ys = [s(i) for i in x]
    pyplot.plot(x, yf, 'g', x, ys, 'b')
    pyplot.show()
    # проверка производных
    print(
        (s(x_min) - 2 * s(x_min + eps) + s(x_min + 2 * eps)) / (eps * eps),
        (s(x_max) - 2 * s(x_max - eps) + s(x_max - 2 * eps)) / (eps * eps),
        sep=' '
    )
