"""Upload-time experiment: what the numbers are allowed to conclude.

Input is one (slot, views) pair per Short, where views is the count over the same-length window for every
video (publish day through day 7). Shorts views are heavy-tailed, so medians are compared, never means, and a
permutation test asks how often a gap this large appears when slot labels are shuffled.

Decision rule (fixed before the test starts, so it cannot be bent to the result):
  extend         a slot has fewer than MIN_N videos
  keep_baseline  best slot is already a baseline slot, or its lift is under MIN_LIFT, or p > ALPHA
  adopt          otherwise: move to the two best slots, then re-test
A slot effect is a correlation with one channel's first weeks, not a law. Topic and hook differences are
larger than timing differences; the test only says whether timing is visible above that noise.
"""
import random, statistics as st

MIN_N, MIN_LIFT, ALPHA = 7, 0.30, 0.10


def analyze(rows, baseline=("B", "D"), perms=5000, seed=7):
    by = {}
    for slot, v in rows:
        by.setdefault(slot, []).append(float(v))
    summary = {s: {"n": len(v), "median": st.median(v), "min": min(v), "max": max(v)} for s, v in sorted(by.items())}
    out = {"slots": summary, "rule": {"min_n": MIN_N, "min_lift": MIN_LIFT, "alpha": ALPHA}}
    if len(by) < 2 or any(len(v) < MIN_N for v in by.values()):
        out.update(decision="extend", reason=f"need {MIN_N} videos in every slot")
        return out
    order = sorted(by, key=lambda s: summary[s]["median"], reverse=True)
    best = order[0]
    base = st.median([x for s in baseline for x in by.get(s, [])])
    lift = (summary[best]["median"] - base) / base if base else float("inf")
    a, rest = by[best], [x for s in by if s != best for x in by[s]]
    obs = st.median(a) - st.median(rest)
    rng, pool, hits = random.Random(seed), a + rest, 0
    for _ in range(perms):
        rng.shuffle(pool)
        if abs(st.median(pool[: len(a)]) - st.median(pool[len(a):])) >= abs(obs):
            hits += 1
    p = (hits + 1) / (perms + 1)
    out.update(best=best, ranking=order, baseline_median=base, lift=round(lift, 3), p_value=round(p, 4))
    if best in baseline:
        out.update(decision="keep_baseline", reason="the best slot is already in the baseline pair")
    elif lift < MIN_LIFT or p > ALPHA:
        out.update(decision="keep_baseline", reason="difference is too small or too likely to be noise")
    else:
        out.update(decision="adopt", new_slots=order[:2], reason="best slot beats baseline by the pre-set margin")
    return out


def rows_from_db(c, experiment_id, metric="views_d0_d7"):
    q = """SELECT p.slot, a.value FROM publications p JOIN analytics a ON a.youtube_id=p.youtube_id
           WHERE p.experiment_id=? AND a.metric=? AND p.status='live'"""
    return [(r["slot"], r["value"]) for r in c.execute(q, (experiment_id, metric))]
