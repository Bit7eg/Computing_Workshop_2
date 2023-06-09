import sys

import matrix.functions as matrix

if __name__ == '__main__':
    if len(sys.argv) > 1:
        matrix.eigenvalues_accuracy = float(sys.argv[1])
        matrix.optimal_accuracy = float(sys.argv[2])
        matrix.seidel_accuracy = float(sys.argv[3])

    a_matrix, b_vector = matrix.get_input()

    eigenvalues = matrix.get_eigenvalues(a_matrix)
    print("Eigenvalues:", end=" ")
    for i in eigenvalues:
        print("{0:.15}".format(i), end="\n")
    print()

    x = matrix.solve_system_optimal(a_matrix, b_vector)
    print("Optimal roots:", end=" ")
    for i in x:
        print("{0:.10}".format(i), end=" ")
    print()

    x = matrix.solve_system_Seidel(a_matrix, b_vector)
    print("Seidel roots:", end=" ")
    for i in x:
        print("{0:.10}".format(i), end=" ")
    print()