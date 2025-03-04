from my_io import *
from algo import *
from greeting import greet

def main():
    greet()
    while True:
        try:
            input_choice = input_method_choice([1, 2, 3])
            if input_choice == 2:
                filename = input("Введите имя файла: ").strip()
                A, b, tol, x0 = file_matrix_input(filename)
            elif input_choice == 1:
                A, b, tol, x0 = cli_matrix_input()
            elif input_choice == 3:
                A, b, tol, x0 = random_matrix_input()

            max_iter = 10000;
            try:
                x, errors, iterations = solve(A, b, x0, tol, max_iter)
            except TypeError:
                continue

            output_choice = output_method_choice([1, 2])
            if output_choice == 1:
                print("Решение:", x)
                print("Число итераций:", iterations)
                print("Вектор погрешностей:", errors)
            else:
                while True:
                    out_filename = input("Введите имя файла для сохранения: ").strip()
                    try:
                        with open(out_filename, 'w') as f:
                            f.write(f"Решение: {x}\n")
                            f.write(f"Число итераций: {iterations}\n")
                            f.write(f"Вектор погрешностей: {errors}\n")
                        print("Ответ записан в файл.")
                        break
                    except OSError:
                        print("Ошибка записи в файл. Попробуйте снова.")
            print("\n -------------------------- \n")

        except KeyboardInterrupt:
            print("\nВыход из программы.")
            exit()
    
if __name__ == "__main__":
    main()
