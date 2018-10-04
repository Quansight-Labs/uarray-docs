import pathlib
import perf
from collections import defaultdict
from matplotlib import pyplot as plt
import numpy as np

def get_items():
    for path in pathlib.Path('.').glob("*.json"):
        try:
            _, reduced = path.stem.split('-', 2)
        except ValueError:
            continue
        is_reduced = reduced == 'reduced'
        benchmark = perf.Benchmark.load(str(path))
        n = int(benchmark.get_name())
        for value in benchmark.get_values():
            yield {"n": n, "time": value * 1000, "reduced": is_reduced}


def main():
    _reduced = defaultdict(list)
    _original = defaultdict(list)
    for items in get_items():
        (_reduced if items['reduced'] else _original)[items['n']].append(items['time'])

    reduced_n = np.array(sorted(_reduced))
    reduced_time = np.zeros(len(reduced_n))
    for i,n in enumerate(reduced_n):
        reduced_time[i] = np.mean(_reduced[n])

    original_n = np.array(sorted(_original))
    original_time = np.zeros(len(original_n))
    for i,n in enumerate(original_n):
        original_time[i] = np.mean(_original[n])

    assert (reduced_n == original_n).all()
    n = reduced_n
    
    def original_nops(n):
        'the number of arithmetic operations in original expression'
        return (5*n)**2 + 5*n + 5*n-1.

    def reduced_nops(n):
        'the number of arithmetic operations in reduced expression'
        return 5*n + 5*n-1 + 1.

    poly = np.polyfit(reduced_n, original_time/reduced_time, 2)
    # Speedup plot.
    plt.figure()
    plt.plot(reduced_n, np.polyval(poly, reduced_n), label='quadratic')
    plt.plot(n, original_time/reduced_time, label='measured')
    plt.ylabel('Speedup factor')
    plt.xlabel('Size parameter, n')
    plt.legend()
    plt.savefig('speedup.png')
    plt.show()

    # Timing plot
    plt.figure()
    plt.plot(n, original_time, label='original')
    plt.plot(n, reduced_time, label='reduced')
    plt.ylabel('Time taken')
    plt.xlabel('Size parameter, n')
    plt.legend()
    plt.savefig('timing.png')
    plt.show()
    
if __name__ == '__main__':
    main()
