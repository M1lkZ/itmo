def is_diagonally_dominant(A):
    n = len(A)
    for i in range(n):
        row_sum = sum(abs(A[i][j]) for j in range(n) if j != i)
        if abs(A[i][i]) < row_sum:
            return False
    return True

def permute_rows_and_columns(A, b):
    n = len(A)
    for i in range(n):
        max_val = 0
        max_idx = i
        for j in range(i, n):
            if abs(A[j][i]) > max_val:
                max_val = abs(A[j][i])
                max_idx = j
        if max_idx != i:
            # Переставляем строки
            A[[i, max_idx]] = A[[max_idx, i]]
            b[[i, max_idx]] = b[[max_idx, i]]
    return A, b


def gauss_seidel(A, b, x0, epsilon, max_iterations):
    try:
        n = len(A)
        x = x0.copy()
        errors = []

        for k in range(max_iterations):
            delta = 0
            for i in range(n):
               s = sum(A[i][j] * x[j] for j in range(i)) + sum(A[i][j] * x0[j] for j in range(i + 1, n))
               new_xi = (b[i] - s) / A[i][i]
               d = abs(new_xi - x0[i])
               if d > delta:
                   delta = d
                   x[i] = new_xi
            errors.append(delta)
        
            if delta < epsilon:
                return x, errors[-1], k + 1
            x0 = x.copy()

        return None, [], 0

    except:
        print("Неизвестная ошибка в рассчётах.")

def solve(A, b, x0, tol, max_iter):
    if not is_diagonally_dominant(A):
        print("Матрица не имеет диагонального преобладания. Попытка перестановки строк.")
        A, b = permute_rows_and_columns(A, b)
        if not is_diagonally_dominant(A):
            print("Не удалось достичь диагонального преобладания. Корректный ответ не гарантирован.")
        x, errors, iterations = gauss_seidel(A, b, x0, tol, max_iter)
        while x is None:
            print("Произошла неизвестная ошибка. Попробуйте ввести данные снова.")
            A, b, tol = cli_matrix_input()
            x, errors, iterations = gauss_seidel(A, b, x0, tol, max_iter)
        return x, errors, iterations