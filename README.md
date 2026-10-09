# Week 4 – Performance Optimization in Python

Pure standard-library project (Python 3.9+), no input files required – all data is generated
deterministically by `data_generator.py`.

| File | Purpose |
|---|---|
| `original/app_original.py` | Baseline (unoptimized) application |
| `optimized/app_optimized.py` | Optimized application, identical results |
| `data_generator.py` | Seeded synthetic data (transactions, texts, numeric series) |
| `tests/test_equivalence.py` | 8 unittest cases proving original == optimized |
| `benchmark.py` | timeit + cProfile + tracemalloc harness |
| `run_all.py` | Runs tests then benchmark |
| `results/` | Saved cProfile output and `benchmark.json` from the report run |

Run: `python run_all.py` (or `python tests/test_equivalence.py`, `python benchmark.py`).
