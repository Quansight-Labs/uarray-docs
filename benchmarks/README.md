# Benchmarks


There are some benchmarks setup with the [perf](https://github.com/vstinner/perf) module.

```bash
# install perf and python3 and numpy
conda env create -f environment.yml
conda activate uarray-docs

# Clean out old values
make clean

# tune system
# https://perf.readthedocs.io/en/latest/system.html
python3 -m perf system tune

# run benchmarks
make all

# look at comparisons
make compare
```

Then run `jupyter lab` and open `Make Graph` to create graphs.
