"""One-command runner: tests -> benchmark. Usage: python run_all.py"""
import subprocess, sys
for cmd in ([sys.executable, "tests/test_equivalence.py"], [sys.executable, "benchmark.py"]):
    if subprocess.call(cmd) != 0: sys.exit(1)
