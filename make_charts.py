"""Optional: builds charts from results/benchmark.json (needs matplotlib)."""
import json, os
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
d = json.load(open(os.path.join(R, "benchmark.json")))
names = list(d["per_function"]); o = [d["per_function"][n]["original_s"]*1000 for n in names]
p = [d["per_function"][n]["optimized_s"]*1000 for n in names]
fig, ax = plt.subplots(figsize=(9, 4.6)); x = range(len(names)); w = .38
ax.bar([i-w/2 for i in x], o, w, label="Original", color="#c0392b")
ax.bar([i+w/2 for i in x], p, w, label="Optimized", color="#2e86c1")
ax.set_yscale("log"); ax.set_ylabel("Time (ms, log scale)"); ax.set_xticks(list(x))
ax.set_xticklabels(names, rotation=30, ha="right", fontsize=8); ax.legend(); ax.set_title("Per-function execution time")
plt.tight_layout(); plt.savefig(os.path.join(R, "chart_per_function.png"), dpi=150); plt.close()
fig, ax = plt.subplots(figsize=(5, 4)); wl = d["workload"]
ax.bar(["Original", "Optimized"], [wl["original"]["wall_s"], wl["optimized"]["wall_s"]], color=["#c0392b", "#2e86c1"])
ax.set_ylabel("Seconds"); ax.set_title("Full workload wall time")
for i, v in enumerate([wl["original"]["wall_s"], wl["optimized"]["wall_s"]]): ax.text(i, v, f"{v:.3f}s", ha="center", va="bottom")
plt.tight_layout(); plt.savefig(os.path.join(R, "chart_workload.png"), dpi=150)
