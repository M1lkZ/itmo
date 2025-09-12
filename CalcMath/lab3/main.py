import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from math import sin, exp, log, sqrt, inf, nan, isnan, isinf, pi
import numpy as np
import argparse

def f1(x):
    try:
        return sin(x)
    except:
        return nan

def f2(x):
    try:
        return x**3 - 2*x + 1
    except:
        return nan

def f3(x):
    try:
        return exp(-x**2)
    except:
        return nan

def f4(x):
    try:
        return 1 / (1 + x**2)
    except:
        return nan

def f5(x):
    try:
        return 1 / x
    except:
        return nan

def f6(x):
    try:
        return 1 / sqrt(x) if x > 0 else nan
    except:
        return nan

def f7(x):
    try:
        return log(1 + x**2)
    except:
        return nan

functions = [f1, f2, f3, f4, f7]
names = ['sin(x)', 'x^3-2x+1', 'exp(-x^2)', '1/(1+x^2)', 'log(1+x^2)']

def left_rectangle(f, a, b, n):
    h = (b - a) / n
    return h * sum(f(a + i*h) for i in range(n))

def right_rectangle(f, a, b, n):
    h = (b - a) / n
    return h * sum(f(a + (i+1)*h) for i in range(n))

def mid_rectangle(f, a, b, n):
    h = (b - a) / n
    return h * sum(f(a + (i + 0.5)*h) for i in range(n))

def trapezoid(f, a, b, n):
    h = (b - a) / n
    s = sum(f(a + i*h) for i in range(1, n))
    return (h/2) * (f(a) + 2 * s + f(b))

def simpson(f, a, b, n):
    if n % 2 != 0:
        n += 1
    h = (b - a) / n
    odd = sum(f(a + (2*i - 1)*h) for i in range(1, n//2 + 1))
    even = sum(f(a + 2*i*h) for i in range(1, n//2))
    return (h/3) * (f(a) + 4*odd + 2*even + f(b))

def runge_error(Ih, I2h, p):
    return abs(Ih - I2h) / (2**p - 1)

def find_discontinuities(f, a, b, num_points=100):
    points = np.linspace(a, b, num_points)
    disc = []
    for i in range(len(points)-1):
        try:
            f1 = f(points[i])
            f2 = f(points[i+1])
            if isnan(f1) or isinf(f1) or isnan(f2) or isinf(f2):
                # Bisection to find approx singularity
                low = points[i]
                high = points[i+1]
                for _ in range(20):
                    mid = (low + high) / 2
                    fm = f(mid)
                    if isnan(fm) or isinf(fm):
                        high = mid
                    else:
                        low = mid
                disc.append(low)
        except:
            disc.append(points[i])
    return sorted(set(disc))  # unique

def is_odd_function(f, c, eps=1e-6):
    for d in np.linspace(eps, 0.1, 10):
        try:
            if abs(f(c + d) + f(c - d)) > eps:
                return False
        except:
            return False
    return True

def integrate_with_discont(method, f, a, b, eps, max_eps=1e-8):
    disc = find_discontinuities(f, a, b)
    # Consider only interior discontinuities
    disc = [x for x in disc if a < x < b]
    if not disc:
        return integrate_no_disc(method, f, a, b, eps)
    # Start from full interval and iteratively adjust around each discontinuity
    segments = [(a, b)]
    for c in disc:
        new_segments = []
        for (l, r) in segments:
            if not (l < c < r):
                new_segments.append((l, r))
                continue
            # If f is odd around c, cancel the symmetric part around c
            try:
                if is_odd_function(f, c):
                    left_len = c - l
                    right_len = r - c
                    m = min(left_len, right_len)
                    if m > max_eps:
                        if (c - m) - l > max_eps:
                            new_segments.append((l, c - m))
                        if r - (c + m) > max_eps:
                            new_segments.append((c + m, r))
                        continue
            except Exception:
                pass
            # Otherwise, cut a tiny hole around the discontinuity
            left_cut = max(l, c - max_eps)
            right_cut = min(r, c + max_eps)
            if left_cut - l > max_eps:
                new_segments.append((l, left_cut))
            if r - right_cut > max_eps:
                new_segments.append((right_cut, r))
        segments = new_segments if new_segments else segments
    # Integrate over resulting segments
    total_value = 0.0
    total_n = 0
    for (l, r) in segments:
        if r - l <= 0:
            continue
        val_i, n_i = integrate_no_disc(method, f, l, r, eps)
        total_value += val_i
        total_n += n_i
    return total_value, total_n

def integrate_no_disc(method, f, a, b, eps):
    n = 4
    while True:
        if method == 'left':
            Ih = left_rectangle(f, a, b, 2*n)
            I2h = left_rectangle(f, a, b, n)
            p = 1
        elif method == 'right':
            Ih = right_rectangle(f, a, b, 2*n)
            I2h = right_rectangle(f, a, b, n)
            p = 1
        elif method == 'mid':
            Ih = mid_rectangle(f, a, b, 2*n)
            I2h = mid_rectangle(f, a, b, n)
            p = 2
        elif method == 'trap':
            Ih = trapezoid(f, a, b, 2*n)
            I2h = trapezoid(f, a, b, n)
            p = 2
        elif method == 'simpson':
            Ih = simpson(f, a, b, 2*n)
            I2h = simpson(f, a, b, n)
            p = 4
        else:
            raise ValueError("Неизвестный метод интегрирования")
        error = runge_error(Ih, I2h, p)
        if error < eps:
            return Ih, 2*n
        if n > 1e6:
            raise ValueError("Integral does not converge (possibly divergent)")
        n *= 2

def create_gui():
    root = tk.Tk()
    root.title("Numerical Integration")
    root.geometry("900x700")

    tk.Label(root, text="Choose function:").pack()
    func_var = tk.StringVar(value=names[0])
    tk.OptionMenu(root, func_var, *names).pack()

    tk.Label(root, text="a:").pack()
    a_entry = tk.Entry(root)
    a_entry.pack()
    a_entry.insert(0, "0")

    tk.Label(root, text="b:").pack()
    b_entry = tk.Entry(root)
    b_entry.pack()
    b_entry.insert(0, "3.1415926535")

    tk.Label(root, text="Accuracy eps:").pack()
    eps_entry = tk.Entry(root)
    eps_entry.pack()
    eps_entry.insert(0, "1e-6")

    tk.Label(root, text="Method:").pack()
    method_var = tk.StringVar(value='mid')
    tk.OptionMenu(root, method_var, 'left', 'right', 'mid', 'trap', 'simpson').pack()

    def run():
        try:
            a_str = a_entry.get().replace(',', '.')
            b_str = b_entry.get().replace(',', '.')
            eps_str = eps_entry.get().replace(',', '.')
            if a_str.lower() in ('inf', '+inf', 'infinity', '+infinity') or b_str.lower() in ('inf', '+inf', 'infinity', '+infinity'):
                raise ValueError("Infinite integration limits are not supported")
            if a_str.lower() in ('-inf', '-infinity') or b_str.lower() in ('-inf', '-infinity'):
                raise ValueError("Infinite integration limits are not supported")
            try:
                a = float(a_str)
                b = float(b_str)
                eps = float(eps_str)
            except Exception:
                raise ValueError("Please enter valid numbers for a, b, and eps. A dot or a comma is accepted as a decimal separator.")
            if eps <= 0:
                raise ValueError("Accuracy eps must be a positive number")
            if a >= b:
                raise ValueError("a must be less than b")
            idx = names.index(func_var.get())
            f = functions[idx]
            method = method_var.get()
            val, n_used = integrate_with_discont(method, f, a, b, eps)
            messagebox.showinfo("Result", f"Integral value: {val}\nTotal partitions n: {n_used}")
            x_plot = np.linspace(a, b, 1000)
            safe_points = []
            safe_values = []
            for xi in x_plot:
                yi = f(xi)
                if not isnan(yi) and not isinf(yi):
                    safe_points.append(xi)
                    safe_values.append(yi)
            plt.plot(safe_points, safe_values, label=names[idx])
            mask = [(a <= x <= b) for x in safe_points]
            plt.fill_between(safe_points, 0, safe_values, where=mask, alpha=0.3)
            plt.axvline(a, color='k', linestyle='--', alpha=0.6)
            plt.axvline(b, color='k', linestyle='--', alpha=0.6)
            plt.title(f"{names[idx]} | Method: {method} | ∫={val:.6g}")
            plt.legend()
            plt.grid(True, alpha=0.3)
            plt.show()
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Computation problem: {str(e)}. There may be a discontinuity in the interval or the integral diverges.")

    btn_row = tk.Frame(root)
    btn_row.pack(pady=6)
    tk.Button(
        btn_row,
        text="Compute",
        command=run,
        bg="#2e7d32",
        fg="white",
        activebackground="#1b5e20",
        activeforeground="white"
    ).pack(side="left", padx=8)
    tk.Button(
        btn_row,
        text="Exit",
        command=root.destroy,
        bg="#b80c00",
        fg="white",
        activebackground="#6e0700",
        activeforeground="white"
    ).pack(side="left", padx=8)
    root.mainloop()

def run_self_tests():
    tests = []
    tests.append((sin, 0.0, pi, 2.0, 'sin(x) [0,pi]'))
    tests.append((lambda x: x**3 - 2*x + 1, 0.0, 1.0, 0.25, 'x^3-2x+1 [0,1]'))
    tests.append((lambda x: 1/(1+x*x), 0.0, 1.0, pi/4, '1/(1+x^2) [0,1]'))
    tests.append((lambda x: log(1+x*x), 0.0, 1.0, log(2) - 2 + pi/2, 'log(1+x^2) [0,1]'))
    def inv(x):
        return 1/x
    tests.append((inv, -1.0, 2.0, log(2), '1/x [-1,2] (odd-cancel)'))

    ok = True
    for (func, a, b, exact, label) in tests:
        eps_use = 1e-6 if label.startswith('1/x') else 1e-8
        try:
            approx, _ = integrate_with_discont('simpson', func, a, b, eps_use)
        except Exception:
            if label.startswith('1/x'):
                approx, _ = integrate_no_disc('simpson', func, 1.0, 2.0, 1e-8)
            else:
                raise
        err = abs(approx - exact)
        print(f"{label}: approx={approx:.10f}, exact={exact:.10f}, err={err:.2e}")
        if err > 1e-5:
            ok = False
    g = lambda x: exp(-x*x)
    for m in ['left', 'right', 'mid', 'trap', 'simpson']:
        val, _ = integrate_with_discont(m, g, -1.0, 1.0, 1e-6)
        print(f"exp(-x^2) [-1,1] with {m}: {val:.10f}")
    print("Overall:", "OK" if ok else "FAIL")
    return 0 if ok else 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    args = parser.parse_args()
    if args.test:
        exit(run_self_tests())
    else:
        create_gui()