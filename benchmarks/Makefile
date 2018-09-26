.PHONY: clean all compare

all_targets = %-0-original-dask.json %-1-original-tensordot.json %-2-original.json %-3-reduced-dask.json %-4-reduced-tensordot.json %-5-reduced.json

.PRECIOUS: $(all_targets)

setup = import numpy as np; n = $*; shape = (2 * n, 3 * n, 5 * n) ; A = np.arange(np.prod(shape)).reshape(shape); B = 2 + A
setup_dask = import numpy as np; import dask.array as da; n = $*; shape = (2 * n, 3 * n, 5 * n) ; A = da.arange(np.prod(shape), chunks=1000).reshape(shape); B = 2 + A

benchmark_command = python3 -m perf timeit --rigorous -o $@ --name=$*

# benchmark_targets = benchmarks/original_1.json benchmarks/reduced_1.json benchmarks/original_10.json benchmarks/reduced_10.json benchmarks/original_100.json  benchmarks/reduced_100.json

# numbered order from slowest to fastest so they sort in comparisons

%-0-original-dask.json:
	$(benchmark_command) -s '$(setup_dask); res = da.tensordot(A[1,0,:], da.outer(A[1,0,:], B[0,1,:])[2,:], axes=(-1,-1))' 'res.compute()'

%-1-original-tensordot.json:
	$(benchmark_command) -s '$(setup)' 'np.tensordot(A[1,0,:], np.outer(A[1,0,:], B[0,1,:])[2,:], axes=(-1,-1))'


%-2-original.json:
	$(benchmark_command) -s '$(setup)' 'np.inner(A[1,0,:], np.outer(A[1,0,:], B[0,1,:])[2,:])'


%-3-reduced-dask.json:
	$(benchmark_command) -s '$(setup_dask); res = da.tensordot(A[1,0,:], B[0,1,:], axes=(-1,-1)) * A[1,0,2]' 'res.compute()'

%-4-reduced-tensordot.json:
	$(benchmark_command) -s '$(setup)' 'np.tensordot(A[1,0,:], B[0,1,:], axes=(-1,-1)) * A[1,0,2]'


%-5-reduced.json:
	$(benchmark_command) -s '$(setup)' 'np.inner(A[1,0,:], B[0,1,:]) * A[1,0,2]'


%-all: FORCE $(all_targets)
	@echo done $*

%-all-dask: FORCE %-0-original-dask.json %-3-reduced-dask.json
	@echo done dask $*

all: 1-all 10-all 100-all 1000-all-dask 10000-all-dask
	@echo done all

compare_%: FORCE
	python3 -m perf compare_to $*-*.json

compare: compare_1 compare_10 compare_100 compare_1000 compare_10000
	@echo compared

clean: FORCE
	rm *.json

FORCE: