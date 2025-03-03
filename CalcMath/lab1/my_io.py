import numpy as np
np.seterr(all='raise')

def input_method_choice(valid_inputs):
    while True:
        inp = int(input("Выберите метод ввода: 1 - вручную, 2 - из файла: "))
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

def file_matrix_input(filename):
    while True:
        try:
            with open(filename, 'r') as f:
                n = int(f.readline().strip())
                if n > 20:
                    raise ValueError("Размерность матрицы не должна превышать 20.")
                A = [list(map(float, f.readline().split())) for _ in range(n)]
                b = list(map(float, f.readline().split()))
                if len(A) != n or len(b) != n:
                    raise ValueError("Размерность матрицы или вектора не соответствует заданной.")
                tol = float(f.readline().strip())
                if tol <= 0:
                    raise ValueError("Точность должна быть положительным числом.")
                x0 = list(map(float, f.readline().split()))
                if len(x0) != n:
                    raise ValueError("Размерность вектора приближений не соответствует заданной.")
                max_iter = int(f.readline().strip())
            return np.array(A, dtype = float), np.array(b, dtype = float), tol, np.array(x0, dtype = float), max_iter
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
            A = [list(map(float, input().split())) for _ in range(n)]
            print("Введите вектор b через пробел:")
            b = list(map(float, input().split()))
            if len(A) != n or len(b) != n:
                raise ValueError("Размерность матрицы или вектора не соответствует заданной.")
            tol = float(input("Введите точность вычислений: ").strip())
            if tol <= 0:
                    raise ValueError("Точность должна быть положительным числом.")
            x0 = list(map(float, input("Введите вектор приближений через пробел: ").split()))
            if len(x0) != n:
                raise ValueError("Размерность вектора приближений не соответствует заданной.")
            max_iter = int(input("Введите максимальное число итераций: ").strip())
            return np.array(A, dtype = float), np.array(b, dtype = float), tol, np.array(x0, dtype = float), max_iter
        except ValueError as e:
            print(f"Ошибка: {e} Попробуйте снова.")