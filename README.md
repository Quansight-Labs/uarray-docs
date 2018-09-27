# uarray-docs
A collection of LaTeX documents relating to Mathematics of Arrays formalism and the UArray project.


[![CircleCI](https://circleci.com/gh/Quansight-Labs/uarray-docs/tree/master.svg?style=svg)](https://circleci.com/gh/Quansight-Labs/uarray-docs/tree/master)


The latex documents are built in CircleCi and available under the Artifacts tab of any successful build. 

You can also view them [on Overleaf](https://v2.overleaf.com/read/fwvbzwwmkpyb) which is linked to this repo.


## Benchmarks

There are some benchmarks setup with the [perf](https://github.com/vstinner/perf) module.

```bash
cd benchmarks
conda env create -f environment.yml
conda activate uarray-docs
make all
make compare
```