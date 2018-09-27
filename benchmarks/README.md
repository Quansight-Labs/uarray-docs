# Benchmarks


There are some benchmarks setup with the [perf](https://github.com/vstinner/perf) module.

```bash
conda env create -f environment.yml
conda activate uarray-docs
# Clean out old values
make clean
# run benchmarks
make all
# look at comparisons
make compare
```

Then run `jupyter lab` and open `Make Graph` to create graphs.