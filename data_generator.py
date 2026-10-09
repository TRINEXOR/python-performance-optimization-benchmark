"""Deterministic synthetic data generator (no external input files needed)."""
import random

WORDS = ("alpha beta gamma delta epsilon zeta eta theta iota kappa lambda mu nu xi omicron "
         "pi rho sigma tau upsilon phi chi psi omega data cache loop sort heap graph tree "
         "queue stack index query batch stream").split()


def generate_transactions(n=3000, n_customers=300, seed=42):
    """Return list of dicts: id, customer, amount. ~2% of ids are deliberately duplicated."""
    rnd = random.Random(seed)
    records = []
    for i in range(n):
        records.append({"id": i, "customer": f"C{rnd.randrange(n_customers):04d}",
                        "amount": round(rnd.uniform(1, 500), 2)})
    for _ in range(n // 50):  # inject duplicates
        records.append(dict(records[rnd.randrange(n)]))
    rnd.shuffle(records)
    return records


def generate_texts(n_docs=400, words_per_doc=60, seed=7):
    rnd = random.Random(seed)
    return [" ".join(rnd.choice(WORDS) + (str(rnd.randrange(30)) if rnd.random() < .5 else "")
                     for _ in range(words_per_doc)) for _ in range(n_docs)]


def generate_series(n=20000, seed=11):
    rnd = random.Random(seed)
    return [round(rnd.uniform(0, 100), 3) for _ in range(n)]
