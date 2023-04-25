import numpy as np

eigenvalues_accuracy = 0.001
seidel_accuracy = 0.001
optimal_accuracy = 0.001

def vector_norm(vector):
    return np.sqrt(sum([i*i for i in vector]))

def transform(source, matrix, offset):
    n = len(source)
    temp = [sum([i[j]*source[j] for j in range(n)]) for i in matrix]
    return [temp[i] - offset[i] for i in range(n)]

def get_input():
    f = open("test3.dat", "r")

    n = int(f.readline())
    a_matrix = [[float(f.readline()) for j in range(n)] for i in range(n)]
    b_vector = [float(f.readline()) for i in range(n)]

    f.close()

    return a_matrix, b_vector

def get_eigenvalues(matrix):
    a = [[j for j in i] for i in matrix]
    n = len(a)
    delta = max([sum([np.abs(j) for j in a[i]]) - np.abs(a[i][i]) for i in range(n)])
    iters = 0
    while eigenvalues_accuracy < delta:
        for i in range(n):
            max_index = int(i == 0)
            for j in range(n):
                if (i != j) and (np.abs(a[i][j]) > np.abs(a[i][max_index])):
                    max_index = j
            tau = (a[i][i] - a[max_index][max_index])/a[i][max_index]
            if tau > 0: t = 1.0/(tau + np.sqrt(tau*tau + 1))
            elif tau < 0: t = 1.0/(tau - np.sqrt(tau*tau + 1))
            else: t = 1.0
            c = 1/np.sqrt(t*t + 1)
            s = t*c
            buff = [[j for j in i] for i in a]
            buff[i] = [c*a[i][j] + s*a[max_index][j] for j in range(n)]
            buff[max_index] = [c*a[max_index][j] - s*a[i][j] for j in range(n)]
            a = [[k for k in j] for j in buff]
            for j in range(n):
                a[j][i] = c*buff[j][i] + s*buff[j][max_index]
                a[j][max_index] = c*buff[j][max_index] - s*buff[j][i]
        delta = max([sum([np.abs(j) for j in a[i]]) - np.abs(a[i][i]) for i in range(n)])
        iters += 1
    print("Eigenvalues iters:", iters)
    return [a[i][i] for i in range(n)]

def solve_system_optimal(a_matrix, b_vector):
    n = len(b_vector)
    eigenvalues = get_eigenvalues(a_matrix)
    max_eigen = max(eigenvalues) + 2*eigenvalues_accuracy
    min_eigen = min(eigenvalues) - 2*eigenvalues_accuracy
    tau = 2.0/(max_eigen + min_eigen)
    matrix = [[float(i==j) - tau*a_matrix[i][j] for j in range(n)] for i in range(n)]
    vector = [tau*i for i in b_vector]
    x = [0 for i in range(n)]
    iters = 0
    while vector_norm(transform(x, a_matrix, b_vector))/min_eigen > optimal_accuracy:
        x = [sum([matrix[i][j]*x[j] for j in range(n)]) + vector[i] for i in range(n)]
        iters += 1
    print("Optimal iters:", iters)
    return x

def solve_system_Seidel(a_matrix, b_vector):
    n = len(b_vector)
    min_eigen = min(get_eigenvalues(a_matrix))
    x = [0 for i in range(n)]
    iters = 0
    while vector_norm(transform(x, a_matrix, b_vector))/min_eigen > seidel_accuracy:
        for i in range(n):
            x[i] = (b_vector[i] - sum([a_matrix[i][j]*x[j] for j in range(i)]) - 
                    sum([a_matrix[i][j]*x[j] for j in range(i+1, n)]))/a_matrix[i][i]
        iters += 1
    print("Seidel iters:", iters)
    return x
