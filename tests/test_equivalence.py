"""Verifies the optimized code gives the same results as the original."""
import os, sys, unittest, math, importlib.util
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, ROOT)

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, path))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

O = load("app_original", "original/app_original.py")
N = load("app_optimized", "optimized/app_optimized.py")
from data_generator import generate_transactions, generate_texts, generate_series


class Equivalence(unittest.TestCase):
    def setUp(self):
        self.rec = generate_transactions(600, 40, seed=1)
        self.txt = generate_texts(50, 30, seed=2)
        self.ser = generate_series(1000, seed=3)

    def test_duplicates(self):
        self.assertEqual(O.find_duplicate_ids(self.rec), N.find_duplicate_ids(self.rec))
        self.assertEqual(N.find_duplicate_ids([]), [])

    def test_words(self):
        self.assertEqual(O.word_frequencies(self.txt), N.word_frequencies(self.txt))
        self.assertEqual(N.word_frequencies([]), [])

    def test_primes(self):
        for lim in (0, 1, 2, 3, 10, 97, 100, 1000, 2000):
            self.assertEqual(O.count_primes(lim), N.count_primes(lim), lim)
        self.assertEqual(N.count_primes(20000), 2262)

    def test_moving_average(self):
        a, b = O.moving_average(self.ser, 25), N.moving_average(self.ser, 25)
        self.assertEqual(len(a), len(b))
        for x, y in zip(a, b):
            self.assertTrue(math.isclose(x, y, rel_tol=1e-9, abs_tol=1e-9))
        self.assertEqual(N.moving_average([1, 2, 3], 5), [])

    def test_top_customers(self):
        self.assertEqual(O.top_customers(self.rec, 7), N.top_customers(self.rec, 7))

    def test_fib(self):
        for n in range(0, 20):
            self.assertEqual(O.fib(n), N.fib(n))
        self.assertEqual(N.fib(50), 12586269025)

    def test_report(self):
        t = O.top_customers(self.rec, 5)
        self.assertEqual(O.build_report(t), N.build_report(t))

    def test_full_workload(self):
        a, b = O.run_workload(), N.run_workload()
        for key in a:
            if key == "moving_avg":
                self.assertEqual(len(a[key]), len(b[key]))
                self.assertTrue(all(math.isclose(x, y, rel_tol=1e-9) for x, y in zip(a[key], b[key])))
            else:
                self.assertEqual(a[key], b[key], key)

if __name__ == "__main__":
    unittest.main(verbosity=2)
