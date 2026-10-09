"""OPTIMIZED version of the data-processing application (same public API & results)."""
import os, sys, heapq
from collections import Counter, defaultdict
from functools import lru_cache
from itertools import accumulate
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from data_generator import generate_transactions, generate_texts, generate_series


def find_duplicate_ids(records):
    # O(n): single pass with a hash-based counter
    counts = Counter(r["id"] for r in records)
    return sorted(i for i, c in counts.items() if c > 1)


def word_frequencies(texts):
    # O(total words): hash lookups via Counter; split+update runs in C
    counts = Counter()
    for text in texts:
        counts.update(text.split())
    return sorted(counts.items(), key=lambda t: (-t[1], t[0]))


def count_primes(limit):
    # Sieve of Eratosthenes: O(n log log n) with a bytearray and slice assignment
    if limit < 2:
        return 0
    sieve = bytearray([1]) * (limit + 1)
    sieve[0:2] = b"\x00\x00"
    for p in range(2, int(limit ** 0.5) + 1):
        if sieve[p]:
            sieve[p * p::p] = bytes(len(range(p * p, limit + 1, p)))
    return sum(sieve)


def moving_average(values, window):
    # prefix sums: O(n) instead of O(n*window)
    prefix = [0.0] + list(accumulate(values))
    return [(prefix[i + window] - prefix[i]) / window for i in range(len(values) - window + 1)]


def top_customers(records, k=5):
    # single pass aggregation + heap-based selection
    sums = defaultdict(float)
    for r in records:
        sums[r["customer"]] += r["amount"]
    totals = [(c, round(s, 2)) for c, s in sums.items()]
    return heapq.nsmallest(k, totals, key=lambda t: (-t[1], t[0]))


@lru_cache(maxsize=None)
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)


def build_report(totals):
    return "".join(f"Rank {rank}: {c} -> {s:.2f}\n" for rank, (c, s) in enumerate(totals, 1))


def run_workload():
    records = generate_transactions()
    texts = generate_texts()
    series = generate_series()
    top = top_customers(records, 10)
    return {
        "duplicates": find_duplicate_ids(records),
        "word_freq_top": word_frequencies(texts)[:10],
        "primes": count_primes(20000),
        "moving_avg": moving_average(series, 200),
        "top_customers": top,
        "fib": fib(27),
        "report": build_report(top),
    }


if __name__ == "__main__":
    r = run_workload()
    print(r["report"]); print("primes:", r["primes"], "fib:", r["fib"], "dups:", len(r["duplicates"]))
