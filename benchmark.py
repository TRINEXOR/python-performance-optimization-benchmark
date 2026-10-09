"""Profiling + benchmarking harness (stdlib only).
Usage: python benchmark.py      -> writes results/*.txt and results/benchmark.json
"""
import cProfile, pstats, io, json, os, sys, timeit, tracemalloc, importlib.util, platform

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
RES = os.path.join(ROOT, "results"); os.makedirs(RES, exist_ok=True)

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, path))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

O = load("app_original", "original/app_original.py")
N = load("app_optimized", "optimized/app_optimized.py")
from data_generator import generate_transactions, generate_texts, generate_series

REC, TXT, SER = generate_transactions(), generate_texts(), generate_series()

def cases(m):
    def fib27():
        if hasattr(m.fib, "cache_clear"): m.fib.cache_clear()   # fair cold-cache timing
        return m.fib(27)
    return {
        "find_duplicate_ids": lambda: m.find_duplicate_ids(REC),
        "word_frequencies":   lambda: m.word_frequencies(TXT),
        "count_primes(20000)": lambda: m.count_primes(20000),
        "moving_average(w=200)": lambda: m.moving_average(SER, 200),
        "top_customers": lambda: m.top_customers(REC, 10),
        "fib(27) cold": fib27,
        "build_report": lambda: m.build_report(m.top_customers(REC, 10)),
    }

def best_time(fn, repeat, number):
    return min(timeit.repeat(fn, repeat=repeat, number=number)) / number

def peak_mem(fn):
    tracemalloc.start(); fn(); _, peak = tracemalloc.get_traced_memory(); tracemalloc.stop()
    return peak / 1024

def profile(label, m):
    pr = cProfile.Profile(); pr.enable(); m.run_workload(); pr.disable()
    s = io.StringIO()
    pstats.Stats(pr, stream=s).strip_dirs().sort_stats("cumulative").print_stats(15)
    with open(os.path.join(RES, f"cprofile_{label}.txt"), "w") as f: f.write(s.getvalue())
    st = pstats.Stats(pr); return st.total_tt, st.total_calls

def main():
    out = {"python": platform.python_version(), "platform": platform.platform(),
           "per_function": {}, "workload": {}}
    co, cn = cases(O), cases(N)
    for name in co:
        slow = best_time(co[name], repeat=3, number=1)
        n = 50 if slow < 0.01 else (5 if slow < 0.2 else 1)
        t_o = best_time(co[name], 5 if n > 1 else 3, n)
        t_n = best_time(cn[name], 5, max(n, 20) if t_o / 1 > 0 else n)
        out["per_function"][name] = {"original_s": t_o, "optimized_s": t_n, "speedup": t_o / t_n,
                                     "mem_orig_kb": peak_mem(co[name]), "mem_opt_kb": peak_mem(cn[name])}
        print(f"{name:26s} orig={t_o*1000:10.3f} ms  opt={t_n*1000:9.3f} ms  x{t_o/t_n:9.1f}")
    for label, m in (("original", O), ("optimized", N)):
        if hasattr(m.fib, "cache_clear"): m.fib.cache_clear()
        r = 3 if label == "original" else 20
        t = best_time(lambda: (m.fib.cache_clear() if hasattr(m.fib, "cache_clear") else None, m.run_workload()), 3, 1) if label == "original" \
            else best_time(lambda: (m.fib.cache_clear(), m.run_workload()), 10, 1)
        pt, calls = profile(label, m)
        out["workload"][label] = {"wall_s": t, "peak_kb": peak_mem(m.run_workload), "profile_calls": calls}
    w = out["workload"]; w["speedup"] = w["original"]["wall_s"] / w["optimized"]["wall_s"]
    print("WORKLOAD", {k: v for k, v in w.items()})
    json.dump(out, open(os.path.join(RES, "benchmark.json"), "w"), indent=2)

if __name__ == "__main__":
    main()
