.PHONY: clean all compare

all_targets = %-original.json %-reduced.json

.PRECIOUS: $(all_targets)

setup = import numpy as np; n = $*; shape = (2 * n, 3 * n, 5 * n) ; A = np.arange(np.prod(shape)).reshape(shape); B = 2 + A
benchmark_command = python3 -m perf timeit --rigorous -o $@ --name=$* # --track-memory
ns = 1 $(shell seq 10 10 200)


%-original.json:
	$(benchmark_command) -s '$(setup)' 'np.inner(A[1,0,:], np.outer(A[1,0,:], B[0,1,:])[2,:])'


%-reduced.json:
	$(benchmark_command) -s '$(setup)' 'np.inner(A[1,0,:], B[0,1,:]) * A[1,0,2]'


%-all: FORCE $(all_targets)
	@echo done $*

all: $(foreach n,$(ns),$(n)-compare)
	@echo done all

%-compare: FORCE %-all
	python3 -m perf compare_to $*-*.json

compare: $(foreach n,$(ns),$(n)-compare)
	@echo compared

clean: FORCE
	rm *.json

FORCE: