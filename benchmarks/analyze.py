import os
import pathlib
import perf
from collections import defaultdict
import matplotlib as mpl
mpl.use('TkAgg')
from matplotlib import pyplot as plt
import numpy as np

def get_items(d):
    for path in pathlib.Path(d).glob("*.json"):
        try:
            _, reduced = path.stem.split('-', 2)
        except ValueError:
            continue
        is_reduced = reduced == 'reduced'
        try:
            benchmark = perf.Benchmark.load(str(path))
        except Exception as msg:
            print(f'Failed to load {path}: {msg}. SKIPPING')
            continue
        n = int(benchmark.get_name())
        for value in benchmark.get_values():
            yield {"n": n, "time": value * 1000, "reduced": is_reduced}

def get_data(d):
    if not os.path.isdir(d):
        return None, None, None
    _reduced = defaultdict(list)
    _original = defaultdict(list)
    for items in get_items(d):
        (_reduced if items['reduced'] else _original)[items['n']].append(items['time'])

    n = np.array(sorted(set(_reduced.keys()).intersection(_original.keys())))

    reduced_time = np.zeros(len(n))
    for i,_n in enumerate(n):
        reduced_time[i] = np.mean(_reduced[_n])

    original_time = np.zeros(len(n))
    for i,_n in enumerate(n):
        original_time[i] = np.mean(_original[_n])    

    return n, original_time, reduced_time
        
def main():
    l1 = 'inner(a,outer(a,a+2)[1])'
    l2 = 'inner(a,outer(a,a+2,out=cache)[1])'
    n1, ot1, rt1 = get_data('.')
    n2, ot2, rt2 = get_data('prealloc')

    def original_nops(n):
        'the number of arithmetic operations in original expression'
        return (5*n)**2 + 5*n + 5*n-1.

    def reduced_nops(n):
        'the number of arithmetic operations in reduced expression'
        return 5*n + 5*n-1 + 1.

    #poly = np.polyfit(reduced_n, original_time/reduced_time, 2)
    # Speedup plot.
    plt.figure()
    #plt.plot(reduced_n, np.polyval(poly, reduced_n), label='quadratic')
    if n1 is not None:
        plt.plot(n1, ot1/rt1, label=l1)
    if n2 is not None:
        plt.plot(n2, ot2/rt2, label=l2)
    plt.ylabel('Speedup factor')
    plt.xlabel('Size parameter, n')
    plt.legend()
    plt.savefig('speedup.png', dpi=400)
    plt.show()

    # Timing plot
    plt.figure()
    if n1 is not None:
        plt.plot(n1, ot1, label='original')
        plt.plot(n1, rt1, label='reduced')
    if n2 is not None:
        plt.plot(n2, ot2, label='original')
        plt.plot(n2, rt2, label='reduced')
    plt.ylabel('Time taken')
    plt.xlabel('Size parameter, n')
    plt.legend()
    plt.savefig('timing.png', dpi=400)
    plt.show()
    
if __name__ == '__main__':
    main()
