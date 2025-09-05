import tkinter as tk
from tkinter import messagebox, filedialog
import matplotlib.pyplot as plt
from math import sin, cos, exp, log, asin as arcsin
import numpy as np

def func1(x):
    return x**3 - 3*x + 1

def phi1(x):
    inside = 3*x -1
    if inside >= 0:
        return inside ** (1/3)
    else:
        return -(-inside) ** (1/3)

def func2(x):
    return sin(x) - 0.5

def phi2(x):
    return arcsin(0.5)
    return x - func2(x)

def func5(x):
    return -0.38 * x**3 - 3.42 * x**2 + 2.51 * x + 8.75

def phi5(x):
    inside = -9 * x**2 + 6.605 * x + 23.026
    if inside >= 0:
        return inside ** (1/3)
    else:
        return - (-inside) ** (1/3)

functions = [func1, func2, func5]
phi_functions = [phi1, phi2, phi5]

def df1(x):
    return 3*x**2 -3

def dphi5(x):
    ins = -9 * x**2 + 6.605 * x + 23.026
    base = abs(ins) ** (-2/3)
    der = -18 * x + 6.605
    return (1/3) * base * der

def bisection(f, a, b, epsilon):
    table = []
    step = 1
    while abs(a - b) > epsilon:
        x = (a + b) / 2
        fa = f(a)
        fb = f(b)
        fx = f(x)
        table.append((step, a, b, x, fa, fb, fx, abs(a-b)))
        if fa * fx > 0:
            a = x
        else:
            b = x
        step += 1
    return table, (a + b)/2

def chord_method(f, a, b, epsilon):
    table = []
    step = 1
    x_prev = a
    max_iter = 100
    while step <= max_iter:
        fa = f(a)
        fb = f(b)
        if abs(fb - fa) < 1e-10:
            x = (a + b) / 2
            fx = f(x)
            table.append((step, a, b, x, fa, fb, fx, abs(x - x_prev)))
            break
        x = b - fb * (b - a) / (fb - fa)
        fx = f(x)
        table.append((step, a, b, x, fa, fb, fx, abs(x - x_prev)))
        if abs(x - x_prev) < epsilon:
            break
        if fa * fx > 0:
            a = x
        else:
            b = x
        x_prev = x
        step += 1
    return table, x

def secant_method(f, a, b, epsilon):
    table = []
    step = 1
    x0 = a
    x1 = b
    max_iter = 100
    while step <= max_iter:
        f0 = f(x0)
        f1 = f(x1)
        if abs(f1 - f0) < 1e-10:
            x2 = (x0 + x1) / 2
            f2 = f(x2)
            table.append((step, x0, x1, x2, f2, abs(x2 - x1)))
            break
        x2 = x1 - f1 * (x1 - x0) / (f1 - f0)
        f2 = f(x2)
        table.append((step, x0, x1, x2, f2, abs(x2 - x1)))
        if abs(x2 - x1) < epsilon:
            break
        x0 = x1
        x1 = x2
        step += 1
    return table, x2

def simple_iteration(f, phi, a, b, epsilon):
    table = []
    step = 1
    x = (a + b)/2
    max_iter = 100
    while step <= max_iter:
        x_new = phi(x)
        fx_new = f(x_new)
        table.append((step, x, x_new, fx_new, abs(x_new - x)))
        if abs(x_new - x) < epsilon:
            break
        x = x_new
        step += 1
    return table, x_new

def check_convergence(phi_prime, a, b):
    x = np.linspace(a, b, 100)
    max_d = max(abs(phi_prime(xi)) for xi in x)
    return max_d < 1

def system1(x, y):
    return sin(x) + y -1.32, 2*x - cos(y)

def phi_system1(x, y):
    return (cos(y))/2, 1.32 - sin(x)

systems = [system1]
phi_systems = [phi_system1]

def simple_iteration_system(f, phi, x0, y0, epsilon):
    x = x0
    y = y0
    step = 1
    table = []
    while True:
        x_new, y_new = phi(x, y)
        f1, f2 = f(x_new, y_new)
        dx = abs(x_new - x)
        dy = abs(y_new - y)
        table.append((step, x, y, x_new, y_new, f1, f2, max(dx, dy)))
        if max(dx, dy) < epsilon:
            break
        x = x_new
        y = y_new
        step += 1
    return table, x_new, y_new

def check_system_convergence(phi, x0, y0):
    h = 0.01
    px, py = phi(x0, y0)
    px_dx, py_dx = phi(x0 + h, y0)
    px_dy, py_dy = phi(x0, y0 + h)
    J = [[(px_dx - px)/h, (px_dy - px)/h], [(py_dx - py)/h, (py_dy - py)/h]]
    norm = max(abs(J[0][0]) + abs(J[0][1]), abs(J[1][0]) + abs(J[1][1]))
    return norm < 1

def parse_float(value_str):
    if not value_str or not value_str.strip():
        raise ValueError("Empty input")
    
    value_str = value_str.strip()
    
    if value_str.count(' ') > 1:
        raise ValueError(f"Invalid number format: '{value_str}'. Too many spaces.")
    
    if ',' in value_str and '.' not in value_str:
        parts = value_str.split(',')
        if len(parts) == 2:
            if len(parts[1]) == 3 and parts[1].isdigit() and parts[0] != '0':
                value_str = value_str.replace(',', '')
            elif len(parts[1]) <= 3:
                value_str = value_str.replace(',', '.')
            else:
                raise ValueError(f"Invalid number format: '{value_str}'. Invalid comma usage.")
        else:
            raise ValueError(f"Invalid number format: '{value_str}'. Too many commas.")
    
    if ' ' in value_str and '.' in value_str:
        value_str = value_str.replace(' ', '')
    elif ' ' in value_str and ',' in value_str:
        value_str = value_str.replace(' ', '').replace(',', '.')
    elif ' ' in value_str:
        parts = value_str.split(' ')
        if len(parts) == 2 and len(parts[1]) == 3 and parts[1].isdigit():
            value_str = value_str.replace(' ', '')
        else:
            raise ValueError(f"Invalid number format: '{value_str}'. Invalid space usage.")
    
    try:
        return float(value_str)
    except ValueError as e:
        raise ValueError(f"Invalid number format: '{value_str}'. Use point (.) or comma (,) as decimal separator.")

root = tk.Tk()
root.title("Laboratory Work #2")
root.geometry("400x300")

def choose_part():
    part = part_var.get()
    if part == 1:
        equation_window()
    else:
        system_window()

def exit_app():
    root.quit()

tk.Label(root, text="Laboratory Work #2", font=("Arial", 16, "bold")).pack(pady=20)
tk.Label(root, text="Numerical Methods for Solving Nonlinear Equations", font=("Arial", 12)).pack(pady=10)

part_var = tk.IntVar()
part_var.set(1)

tk.Label(root, text="Select part:", font=("Arial", 12, "bold")).pack(pady=10)
tk.Radiobutton(root, text="Nonlinear Equation", variable=part_var, value=1, font=("Arial", 11)).pack(pady=5)
tk.Radiobutton(root, text="System of Nonlinear Equations", variable=part_var, value=2, font=("Arial", 11)).pack(pady=5)

button_frame = tk.Frame(root)
button_frame.pack(pady=20)

tk.Button(button_frame, text="Next", command=choose_part, font=("Arial", 12), 
          bg="lightblue", width=10).pack(side=tk.LEFT, padx=10)
tk.Button(button_frame, text="Exit", command=exit_app, font=("Arial", 12), 
          bg="lightcoral", width=10).pack(side=tk.LEFT, padx=10)

def equation_window():
    eq_win = tk.Toplevel(root)
    eq_win.title("Nonlinear Equation")
    eq_win.geometry("500x600")

    func_var = tk.IntVar()
    tk.Label(eq_win, text="Select function:").pack()
    for i, _ in enumerate(functions, 1):
        tk.Radiobutton(eq_win, text=f"Function {i}", variable=func_var, value=i).pack()

    method_var = tk.IntVar()
    tk.Label(eq_win, text="Select method:").pack()
    tk.Radiobutton(eq_win, text="Chord Method", variable=method_var, value=2).pack()
    tk.Radiobutton(eq_win, text="Secant Method", variable=method_var, value=4).pack()
    tk.Radiobutton(eq_win, text="Simple Iteration", variable=method_var, value=5).pack()

    tk.Label(eq_win, text="Enter parameters:").pack()
    tk.Label(eq_win, text="(Supported formats: 1.5, 1,5, 1 234.56, 1 234,56)", 
             font=("Arial", 9), fg="gray").pack()
    
    # Frame for input fields
    input_frame = tk.Frame(eq_win)
    input_frame.pack(pady=10)
    
    tk.Label(input_frame, text="a:").grid(row=0, column=0, padx=5)
    a_entry = tk.Entry(input_frame, width=10)
    a_entry.grid(row=0, column=1, padx=5)
    a_entry.insert(0, "0")  # Default value
    
    tk.Label(input_frame, text="b:").grid(row=0, column=2, padx=5)
    b_entry = tk.Entry(input_frame, width=10)
    b_entry.grid(row=0, column=3, padx=5)
    b_entry.insert(0, "2")  # Default value
    
    tk.Label(input_frame, text="epsilon:").grid(row=1, column=0, padx=5)
    epsilon_entry = tk.Entry(input_frame, width=10)
    epsilon_entry.grid(row=1, column=1, padx=5)
    epsilon_entry.insert(0, "0.001")  # Default value

    input_var = tk.IntVar()
    tk.Label(eq_win, text="Data input:").pack()
    tk.Radiobutton(eq_win, text="From keyboard", variable=input_var, value=1).pack()
    tk.Radiobutton(eq_win, text="From file", variable=input_var, value=2).pack()

    output_var = tk.IntVar()
    tk.Label(eq_win, text="Output results:").pack()
    tk.Radiobutton(eq_win, text="To screen", variable=output_var, value=1).pack()
    tk.Radiobutton(eq_win, text="To file", variable=output_var, value=2).pack()

    # Output text area
    output_text = tk.Text(eq_win, height=15, width=60)
    output_text.pack(pady=10)
    scrollbar = tk.Scrollbar(eq_win, orient="vertical", command=output_text.yview)
    scrollbar.pack(side="right", fill="y")
    output_text.config(yscrollcommand=scrollbar.set)

    def run_equation():
        f = functions[func_var.get()-1]
        phi = phi_functions[func_var.get()-1]
        method = method_var.get()
        
        output_text.delete(1.0, tk.END)
        
        if input_var.get() == 1:
            try:
                a = parse_float(a_entry.get())
                b = parse_float(b_entry.get())
                epsilon = parse_float(epsilon_entry.get())
            except ValueError as e:
                messagebox.showerror("Error", f"Invalid input: {str(e)}")
                return
        else:
            file = filedialog.askopenfile()
            if file is None:
                return
            lines = file.read().strip().split()
            file.close()
            try:
                a = parse_float(lines[0])
                b = parse_float(lines[1])
                epsilon = parse_float(lines[2])
            except (ValueError, IndexError) as e:
                messagebox.showerror("Error", f"Invalid file: {str(e)}")
                return
        
        if a >= b:
            messagebox.showerror("Error", "a >= b")
            return
        if f(a) * f(b) > 0:
            messagebox.showwarning("Warning", "No root guarantee (f(a)*f(b) >0)")
        
        if method == 5:
            if not check_convergence(dphi5, a, b):
                messagebox.showwarning("Warning", "Convergence condition not met")
        
        # Run method
        if method == 2:
            table, root = chord_method(f, a, b, epsilon)
        elif method == 4:
            table, root = secant_method(f, a, b, epsilon)
        elif method == 5:
            table, root = simple_iteration(f, phi, a, b, epsilon)
        
        num_iter = len(table)
        
        result_text = "Table:\n"
        for row in table:
            result_text += str(row) + '\n'
        result_text += f"\nRoot: {root:.6f}\n"
        result_text += f"f(root): {f(root):.6f}\n"
        result_text += f"Iterations: {num_iter}\n"
        
        output_text.insert(tk.END, result_text)
        
        if output_var.get() == 2:
            with open('output.txt', 'w') as file:
                file.write(result_text)
            messagebox.showinfo("Success", "Results saved to output.txt")
        
        x_plot = np.linspace(a, b, 100)
        y_plot = np.array([f(xi) for xi in x_plot])
        plt.figure(figsize=(8, 6))
        plt.plot(x_plot, y_plot, 'b-', linewidth=2)
        plt.axhline(y=0, color='k', linestyle='-', alpha=0.3)
        plt.axvline(x=root, color='r', linestyle='--', alpha=0.7, label=f'Root: {root:.6f}')
        plt.grid(True, alpha=0.3)
        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.title(f'Function {func_var.get()} - Root Finding')
        plt.legend()
        plt.show()

    button_frame = tk.Frame(eq_win)
    button_frame.pack(pady=10)
    
    def clear_output():
        output_text.delete(1.0, tk.END)
    
    tk.Button(button_frame, text="Execute", command=run_equation, 
              font=("Arial", 12), bg="lightgreen", width=12).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Clear", command=clear_output, 
              font=("Arial", 12), bg="lightyellow", width=12).pack(side=tk.LEFT, padx=5)


def system_window():
    sys_win = tk.Toplevel(root)
    sys_win.title("System of Nonlinear Equations")
    sys_win.geometry("500x600")

    sys_var = tk.IntVar()
    tk.Label(sys_win, text="Select system:").pack()
    for i, _ in enumerate(systems, 1):
        tk.Radiobutton(sys_win, text=f"System {i}", variable=sys_var, value=i).pack()

    method_var = tk.IntVar()
    tk.Label(sys_win, text="Method: Simple Iteration").pack()

    tk.Label(sys_win, text="Enter initial approximations:").pack()
    tk.Label(sys_win, text="(Supported formats: 1.5, 1,5, 1 234.56, 1 234,56)", 
             font=("Arial", 9), fg="gray").pack()
    
    input_frame = tk.Frame(sys_win)
    input_frame.pack(pady=10)
    
    tk.Label(input_frame, text="x0:").grid(row=0, column=0, padx=5)
    x0_entry = tk.Entry(input_frame, width=10)
    x0_entry.grid(row=0, column=1, padx=5)
    x0_entry.insert(0, "0")  # Default value
    
    tk.Label(input_frame, text="y0:").grid(row=0, column=2, padx=5)
    y0_entry = tk.Entry(input_frame, width=10)
    y0_entry.grid(row=0, column=3, padx=5)
    y0_entry.insert(0, "0")  # Default value
    
    tk.Label(input_frame, text="epsilon:").grid(row=1, column=0, padx=5)
    epsilon_entry = tk.Entry(input_frame, width=10)
    epsilon_entry.grid(row=1, column=1, padx=5)
    epsilon_entry.insert(0, "0.001")  # Default value

    output_text = tk.Text(sys_win, height=15, width=60)
    output_text.pack(pady=10)
    scrollbar = tk.Scrollbar(sys_win, orient="vertical", command=output_text.yview)
    scrollbar.pack(side="right", fill="y")
    output_text.config(yscrollcommand=scrollbar.set)

    def run_system():
        f = systems[sys_var.get()-1]
        phi = phi_systems[sys_var.get()-1]
        
        output_text.delete(1.0, tk.END)
        
        try:
            x0 = parse_float(x0_entry.get())
            y0 = parse_float(y0_entry.get())
            epsilon = parse_float(epsilon_entry.get())
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {str(e)}")
            return
        
        if not check_system_convergence(phi, x0, y0):
            messagebox.showwarning("Warning", "Convergence condition not met")
        
        table, x, y = simple_iteration_system(f, phi, x0, y0, epsilon)
        num_iter = len(table)
        f1, f2 = f(x, y)
        
        result_text = "Table:\n"
        for row in table:
            result_text += str(row) + '\n'
        result_text += f"\nSolution: x={x:.6f}, y={y:.6f}\n"
        result_text += f"Residuals: f1={f1:.6f}, f2={f2:.6f}\n"
        result_text += f"Iterations: {num_iter}\n"
        
        output_text.insert(tk.END, result_text)
        
        x_plot = np.linspace(x0 - 1, x0 + 1, 100)
        plt.figure(figsize=(10, 6))
        
        y1_plot = [1.32 - sin(xi) for xi in x_plot]
        y2_plot = [cos(yi)/2 for yi in np.linspace(y0 - 1, y0 + 1, 100)]
        
        plt.subplot(1, 2, 1)
        plt.plot(x_plot, y1_plot, 'b-', label='y = 1.32 - sin(x)')
        plt.axhline(y=y, color='r', linestyle='--', alpha=0.7)
        plt.axvline(x=x, color='r', linestyle='--', alpha=0.7)
        plt.plot(x, y, 'ro', markersize=8, label=f'Solution: ({x:.3f}, {y:.3f})')
        plt.grid(True, alpha=0.3)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('System of Equations')
        plt.legend()
        
        plt.subplot(1, 2, 2)
        plt.plot(x_plot, y2_plot, 'g-', label='x = cos(y)/2')
        plt.axhline(y=y, color='r', linestyle='--', alpha=0.7)
        plt.axvline(x=x, color='r', linestyle='--', alpha=0.7)
        plt.plot(x, y, 'ro', markersize=8, label=f'Solution: ({x:.3f}, {y:.3f})')
        plt.grid(True, alpha=0.3)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('System of Equations')
        plt.legend()
        
        plt.tight_layout()
        plt.show()

    button_frame = tk.Frame(sys_win)
    button_frame.pack(pady=10)
    
    def clear_output():
        output_text.delete(1.0, tk.END)
    
    tk.Button(button_frame, text="Execute", command=run_system, 
              font=("Arial", 12), bg="lightgreen", width=12).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Clear", command=clear_output, 
              font=("Arial", 12), bg="lightyellow", width=12).pack(side=tk.LEFT, padx=5)

root.mainloop()