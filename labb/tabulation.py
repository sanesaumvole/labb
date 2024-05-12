from matplotlib import pyplot as plt

def func(x: list[float]) -> list[float]:
    """
    Calculate function values for passed array of arguments
    """
    a0 = 0.62
    a1 = 0.48
    a2 = 0.38
    N = 3
    
    return [a0 - a1 * abs(t ** (N-1)) - a2 * ((-1) ** (int(2 * t / N))) for t in x]

def tabulate(a: float, b: float, n: int) -> dict[float]:
    x = [a + x * (b - a) / n for x in range(n)]
    y = func(x)
    return (x, y)

def main():
    res = tabulate(0, 1, 1000)

    plt.plot(res[0], res[1])
    plt.grid()
    plt.show()

if __name__ == '__main__':
    main()