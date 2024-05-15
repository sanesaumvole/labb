import numpy as np
import matplotlib.pyplot as plt
import timeit

def func_py(x: float) -> float:
    """
    Calculate function values for passed array of arguments
    """ 
    N = 3
    return 0.62 - 0.48 * abs(x**(N-1)/2) - 0.38 * np.cos(2*np.pi*x/N)

def tabulate_py(a: float, b: float, n: int) -> tuple[list[float], list[float]]:
    x = [a + x*(b - a)/n for x in range(n)]
    y = [func_py(t) for t in x]
    return x, y

def tabulate_np(a: float, b: float, n: int) -> tuple[np.ndarray, np.ndarray]:
    x = np.linspace(a, b, n)
    y = func_py(x)
    return x, y

def main():
    a, b, n = 0, 1, 1000

    n_vals = np.array((1_000, 2_000, 5_000, 10_000, 20_000, 50_000, 100_000), dtype="uint32")
    t_py = np.full_like(n_vals, 0, dtype=float)
    t_np = np.full_like(n_vals, 0, dtype=float)
    for i, n in enumerate(n_vals):
        t_py[i] = 1_000_000 * timeit.timeit(f"tabulate_py(0, 1, {n})", number=100, globals=globals()) / 100
        t_np[i] = 1_000_000 * timeit.timeit(f"tabulate_np(0, 1, {n})", number=100, globals=globals()) / 100

    plt.plot(n_vals, t_py, label='Pure Python')
    plt.plot(n_vals, t_np, label='NumPy')
    plt.xlabel('Number of points')
    plt.ylabel('Time (microseconds)')
    plt.legend()
    plt.grid()
    plt.show()

if __name__ == '__main__':
    main()
