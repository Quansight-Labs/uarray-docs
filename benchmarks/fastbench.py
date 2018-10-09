from timeit import timeit
import numpy as np
from matplotlib import pyplot as plt

nlst = []
t0lst = []
t1lst = []
t2lst = []
t3lst = []

for n in range(10, 210, 10):
    repeat = 10000
    a = np.random.randint(-2**32,2**32-1, size=n, dtype=np.int64)
    b = a + 2
    t0 = timeit('inner(a, outer(a, b)[1])', number=repeat, globals=dict(inner=np.inner, outer=np.outer, a=a, b=b))
    t1 = timeit('outer(a, b)', number=repeat, globals=dict(outer=np.outer, a=a, b=b))
    t2 = timeit('c[1]', number=repeat, globals=dict(c=np.outer(a,b)))
    #t12 = timeit('outer(a, b)[1]', number=repeat, globals=dict(outer=np.outer, a=a, b=b))
    t3 = timeit('inner(a, c)', number=repeat, globals=dict(inner=np.inner, a=a, c=np.outer(a,b)[1]))
    print (n,t0, t1+t2+t3, (t1,t2,t3))
    nlst.append(n)
    t0lst.append(t0)
    t1lst.append(t1)
    t2lst.append(t2)
    t3lst.append(t3)

n = np.array(nlst)
t0 = np.array(t0lst)*1e3
t1 = np.array(t1lst)*1e3
t2 = np.array(t2lst)*1e3
t3 = np.array(t3lst)*1e3


plt.plot(n, t0, label='full')
plt.plot(n, t1, label='outer(a, b)')
plt.plot(n, t2, label='c[1]')
plt.plot(n, t3, label='inner(a, c)')
plt.plot(n, t1+t2+t3, label='sum')
plt.legend()
plt.xlabel('n')
plt.ylabel('timing, ms')
plt.savefig('expr_parts.png')
plt.show()
