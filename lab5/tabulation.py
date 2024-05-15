import numpy as np
from matplotlib import pyplot as plt

def func(x: np.ndarray, a0: float, a1: float, a2: float) -> np.ndarray:
    """
    Calculate function values for passed array of arguments
    """
    return a0 - a1 * np.abs(x - (len(x)-1)/2) - a2 * np.cos(2 * np.pi * x / len(x))

def tabulate_np(a: float, b: float, n: int) -> np.ndarray:
    a0, a1, a2 = 0.62, 0.48, 0.38
    x = np.linspace(a, b, n)
    y = func(x, a0, a1, a2)
    return x, y

def test_tabulation(f, a, b, n, axis):
    res = f(a, b, n)

    axis.plot(res[0], res[1])
    axis.grid()

def main():
    a, b, n = 0, 1, 3

    fig, ax = plt.subplots()
    res = test_tabulation(tabulate_np, a, b, n, ax)
    plt.show()

if __name__ == '__main__':
    main()
