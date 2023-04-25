import numpy as np

def get_equations_system(n, x, k_func, f, formula):
    val_vector = [f(x[i]) for i in range(n)]
    coef_matrix = [[k_func(x[i], x[j]) for j in range(n)] for i in range(n)]

    if formula == "trapezoid":
        for i in range(n):
            coef_matrix[i][0] *= (x[1] - x[0])/2
            for j in range(1, n-1):
                coef_matrix[i][j] *= (x[j+1] - x[j-1])/2
            coef_matrix[i][n-1] *= (x[n-1] - x[n-2])/2
            coef_matrix[i][i] += 1
    else:
        for i in range(n):
            coef_matrix[i][0] = 0
            for j in range(1, n):
                coef_matrix[i][j] *= x[j] - x[j-1]
            coef_matrix[i][i] += 1

    return coef_matrix, val_vector

def solve_system(coef_matrix, val_vector):
    n = len(val_vector)
    buff_matrix = [[j for j in i] for i in coef_matrix]
    buff_vector = [i for i in val_vector]

    for k in range(n-1):
        identity_matrix = [[(0, 1)[i == j] for j in range(n - k)] for i in range(n - k)]
        u = [coef_matrix[i][k] for i in range(k, n)]
        if any([0 != u[i] for i in range(1, n-k)]):
            if u[0] >= 0:
                u[0] += np.sqrt(sum([i*i for i in u]))
            else:
                u[0] -= np.sqrt(sum([i*i for i in u]))
            u_norm = np.sqrt(sum([i*i for i in u]))
            u = [i/u_norm for i in u]
            householder = [[identity_matrix[i][j] - 2*u[i]*u[j] for j in range(n - k)] for i in range(n - k)]
            for i in range(n - k):
                for j in range(n - k):
                    buff_matrix[k+i][k+j] = sum([householder[i][h]*coef_matrix[k+h][k+j] for h in range(n - k)])
                buff_vector[k+i] = sum([householder[i][h]*val_vector[k+h] for h in range(n - k)])
            coef_matrix = [[j for j in i] for i in buff_matrix]
            val_vector = [i for i in buff_vector]

    x = [None for i in range(n)]
    for i in range(n-1, -1, -1):
        x[i] = (val_vector[i] - sum([coef_matrix[i][j]*x[j] for j in range(i+1, n)]))/coef_matrix[i][i]

    return x

def solve_equation_rec(n, x, k_func, f):
    coef_matrix, val_vector = get_equations_system(n, x, k_func, f, "rectangle")
    return solve_system(coef_matrix, val_vector)

def solve_equation_trap(n, x, k_func, f):
    coef_matrix, val_vector = get_equations_system(n, x, k_func, f, "trapezoid")
    return solve_system(coef_matrix, val_vector)