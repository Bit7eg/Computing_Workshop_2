def create(x_arr, y_arr, n, a, b):
    m = [None for i in range(n+1)]
    a_coef = [None for i in range(n+1)]
    b_coef = [None for i in range(n+1)]
    c_coef = [None for i in range(n+1)]
    f_coef = [None for i in range(n+1)]
    h = [None for i in range(n)]
    # инициализация системы
    h[0] = x_arr[1] - x_arr[0]
    b_coef[0] = 1
    c_coef[0] = 0
    f_coef[0] = a
    for i in range(1, n):
        h[i] = x_arr[i+1] - x_arr[i]
        a_coef[i] = h[i-1]/6
        b_coef[i] = (h[i-1] + h[i])/3
        c_coef[i] = h[i]/6
        f_coef[i] = (y_arr[i+1] - y_arr[i])/h[i] - (y_arr[i] - y_arr[i-1])/h[i-1]
    a_coef[n] = 0
    b_coef[n] = 1
    f_coef[n] = b
    # рассчёт вспомогательных констант
    alpha = [None for i in range(n+1)]
    beta = [None for i in range(n+1)]
    alpha[n] = -a_coef[n]/b_coef[n]
    beta[n] = f_coef[n]/b_coef[n]
    for i in range(n-1, 0, -1):
        alpha[i] = -a_coef[i]/(b_coef[i] + c_coef[i]*alpha[i+1])
        beta[i] = (f_coef[i] - c_coef[i]*beta[i+1])/(b_coef[i] + c_coef[i]*alpha[i+1])
    # решение системы
    m[0] = (f_coef[0] - c_coef[0]*beta[1])/(b_coef[0] + c_coef[0]*alpha[1])
    for i in range(1, n+1):
        m[i] = alpha[i]*m[i-1] + beta[i]
    # получение сплайна
    c1 = [None for i in range(n)]
    c2 = [None for i in range(n)]
    for i in range(n):
        c1[i] = (y_arr[i+1] - y_arr[i])/h[i] + h[i]/6 * (m[i] - m[i+1])
        c2[i] = y_arr[i] - m[i]*h[i]*h[i]/6

    def f_spline(x):
        i = 0
        for i in range(n+1):
            if x <= x_arr[i]:
                if x != x_arr[0]:
                    i -= 1
                break

        if i < 0 or i > n-1:
            return None

        h = x_arr[i+1] - x_arr[i]
        return m[i+1]*(x - x_arr[i])**3/(6*h) - m[i]*(x - x_arr[i+1])**3/(6*h) + c1[i]*(x - x_arr[i]) + c2[i]
    return f_spline
