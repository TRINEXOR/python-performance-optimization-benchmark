"""ORIGINAL (baseline) data-processing application -- intentionally unoptimized.

Workloads, each with a deliberate bottleneck:
  1. find_duplicate_ids   - O(n^2) nested loops
  2. word_frequencies     - linear search in a list for every word
  3. count_primes         - trial division by every smaller number
  4. moving_average       - re-sums the whole window for every position
  5. top_customers        - re-scans all records for every customer
  6. fib                  - naive exponential recursion
  7. build_report         - repeated string concatenation
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from data_generator import generate_transactions, generate_texts, generate_series


def find_duplicate_ids(records):
    dups = []
    for i in range(len(records)):
        for j in range(i + 1, len(records)):
            if records[i]["id"] == records[j]["id"] and records[i]["id"] not in dups:
                dups.append(records[i]["id"])
    return sorted(dups)


def word_frequencies(texts):
    table = []  # list of [word, count]
    for text in texts:
        for w in text.split():
            for entry in table:
                if entry[0] == w:
                    entry[1] += 1
                    break
            else:
                table.append([w, 1])
    return sorted(((w, c) for w, c in table), key=lambda t: (-t[1], t[0]))


def is_prime(n):
    if n < 2:
        return False
    for d in range(2, n):
        if n % d == 0:
            return False
    return True


def count_primes(limit):
    return sum(1 for n in range(limit + 1) if is_prime(n))


def moving_average(values, window):
    out = []
    for i in range(len(values) - window + 1):
        total = 0.0
        for k in range(i, i + window):
            total += values[k]
        out.append(total / window)
    return out


def top_customers(records, k=5):
    customers = sorted({r["customer"] for r in records})
    totals = []
    for c in customers:
        s = 0.0
        for r in records:
            if r["customer"] == c:
                s += r["amount"]
        totals.append((c, round(s, 2)))
    totals.sort(key=lambda t: (-t[1], t[0]))
    return totals[:k]


def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)


def build_report(totals):
    report = ""
    for rank, (c, s) in enumerate(totals, 1):
        report += "Rank " + str(rank) + ": " + c + " -> " + "{:.2f}".format(s) + "\n"
    return report


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
