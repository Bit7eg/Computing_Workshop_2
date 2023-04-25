from matplotlib import pyplot
import numpy as np

import constructor.functions as spline

# plot settings
left_coord = 98
right_coord = 152
bottom_coord = 99
top_coord = 103
density = 6000

# spline settings
n = 30000
a = 4
b = -11
x_min = 100
x_max = 150
# eps = 0.00001

# функция для распределения узлов
def get_xi(i):
    return x_min + i * (x_max - x_min)/n

# известная фукнция
def f(x):
    if (x > 130):
        return 100;
    else:
        return 101 + np.sin(x/5.0)


if __name__ == '__main__':
    pyplot.axis([left_coord, right_coord, bottom_coord, top_coord])
    # создание интерполяционной сетки
    x = [get_xi(i) for i in range(n+1)]
    yf = [f(i) for i in x]
    pyplot.scatter(x, yf, s=10, alpha=1, c='r')
    # получение сплайна
    s = spline.create(x, yf, n, a, b)
    # проверка производных
    eps = 1;
    for i in range(1, 9):
        eps = eps/10
        print(
            '{0:.2e} {1:20.10f} {2:20.10f}'.format(
                eps,
                (s(x_min) - 2 * s(x_min + eps) + s(x_min + 2 * eps)) / (eps * eps),
                (s(x_max) - 2 * s(x_max - eps) + s(x_max - 2 * eps)) / (eps * eps)
            )
        )
    # рисование графика
    x = [x_min + i * (x_max - x_min)/(density - 1) for i in range(density)]
    yf = [f(i) for i in x]
    ys = [s(i) for i in x]
    pyplot.plot(x, yf, 'g', x, ys, 'b')
    pyplot.show()
