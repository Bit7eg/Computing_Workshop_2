from matplotlib import pyplot
import numpy as np

import sys_solution.functions as solver

# plot settings
left_coord = -1
right_coord = 4
bottom_coord = -1
top_coord = 4
density = 6000

# solver settings
n = 50
a = 0
b = np.pi

def u_func(x):
    # return np.sin(x)
    # return 3*np.sin(x)**2
    return x

def k_func(x, s):
    # return 2*np.cos(x)*np.cos(s)
    # return np.cos(x)*np.cos(s)
    return s+np.sin(x)

def f_func(x):
    # return np.sin(x)
    # return 3*np.sin(x)**2 + np.cos(x)*(np.sin(b)**3 - np.sin(a)**3)
    return x+(np.pi**2)*(1.0/2.0*np.sin(x)+1.0/3.0*np.pi)

def get_xi(i):
    return a + (i - 1) * (b - a)/(n - 1)

if __name__ == '__main__':
    pyplot.axis([left_coord, right_coord, bottom_coord, top_coord])

    x = [a + i * (b - a)/(density - 1) for i in range(density)]
    y = [u_func(i) for i in x]
    pyplot.plot(x, y, 'b')
    
    x = [get_xi(i) for i in range(1, n+1)]
    # y = solver.solve_equation_rec(n, x, k_func, f_func)
    y = solver.solve_equation_trap(n, x, k_func, f_func)
    pyplot.scatter(x, y, s=10, alpha=1, c='r')

    pyplot.show()
