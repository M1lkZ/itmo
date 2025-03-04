import numpy as np
np.seterr(all='raise')

def input_method_choice(valid_inputs):
    while True:
        inp = int(input("Выберите метод ввода: 1 - вручную, 2 - из файла, 3 - рандом: "))
        if inp not in valid_inputs:
            print("Несуществующий метод, попробуйте снова.")
            continue
        return inp

def output_method_choice(valid_inputs):
    while True:
        inp = int(input("Выберите метод вывода: 1 - в консоль, 2 - в файл: "))
        if inp not in valid_inputs:
            print("Несуществующий метод, попробуйте снова.")
            continue
        return inp

def random_matrix_input():
    while True:
        try:
            n = int(input("Введите размерность матрицы (не более 20): "))
            if n > 20:
                raise ValueError("Размерность матрицы не должна превышать 20.")
            tol = float(input("Введите точность вычислений: ").replace(',', '.').strip())
            if tol <= 0:
                raise ValueError("Точность должна быть положительным числом.")
            low, high = 0.1, 100
            A = np.random.uniform(low, high, (n,n))
            b = np.random.uniform(low, high, (n,1))
            x0 = np.zeros(n)
            print(A)
            print(b)
            return A, b, tol, x0
        except ValueError as e:
            print(f"Ошибка: {e} Попробуйте снова.")

def file_matrix_input(filename):
    while True:
        try:
            with open(filename, 'r') as f:
                n = int(f.readline().strip())
                if n > 20:
                    raise ValueError("Размерность матрицы не должна превышать 20.")
                A = [list(map(float, f.readline().split())) for _ in range(n)]
                b = list(map(float, f.readline().split()))
                if len(A) != n or any(len(row) != n for row in A) or len(b) != n:
                    raise ValueError("Размерность матрицы или вектора не соответствует заданной.")
                tol = float(f.readline().strip())
                if tol <= 0:
                    raise ValueError("Точность должна быть положительным числом.")
                x0 = np.zeros(n)
            return np.array(A, dtype = float), np.array(b, dtype = float), tol, x0
        except (ValueError, FileNotFoundError, IndexError) as e:
            print(f"Ошибка: {e}")
            filename = input("Введите имя файла: ").strip()

def cli_matrix_input():
    while True:
        try:
            n = int(input("Введите размерность матрицы (не более 20): "))
            if n > 20:
                raise ValueError("Размерность матрицы не должна превышать 20.")
            print("Введите матрицу A (значения строк вводите через пробел, новую строку начинайте с помощью Enter):")
            A = [list(map(float, input().replace(',', '.').split())) for _ in range(n)]
            print("Введите вектор b через пробел:")
            b = list(map(float, input().replace(',', '.').split()))
            if len(A) != n or any(len(row) != n for row in A) or len(b) != n:
                raise ValueError("Размерность матрицы или вектора не соответствует заданной.")
            tol = float(input("Введите точность вычислений: ").replace(',', '.').strip())
            if tol <= 0:
                    raise ValueError("Точность должна быть положительным числом.")
            x0 = np.zeros(n)
            return np.array(A, dtype = float), np.array(b, dtype = float), tol, x0
        except ValueError as e:
            print(f"Ошибка: {e} Попробуйте снова.")