"""Topic scoring and duplicate control.

Two models live side by side. v1 is the six-criterion score used in the launch plan (D,C,S,O,V,E, max 100).
v2 is the twelve-criterion weighted model: each criterion is rated 0-10 and missing ones are left out and
the weights re-normalised, so a topic is never given a number for evidence nobody collected.
"""
import json, re
from . import db

WEIGHTS = {"demand": 14, "search": 8, "competition": 8, "outperformance": 10, "novelty": 10, "story": 14,
           "emotion": 8, "evergreen": 8, "relevance": 8, "research": 6, "cost": 3, "monetization": 3}
assert sum(WEIGHTS.values()) == 100
BLOCKING = ("approved", "scheduled", "published", "rejected", "in_production")
STOP = set("a an the of in to it was is what how why did do you your i we like actually really ever for and or with on at as be were from that this".split())


def score(s):
    """s: {criterion: 0..10}. Returns 0..100. Needs criteria covering at least half the weight."""
    bad = [k for k in s if k not in WEIGHTS]
    if bad:
        raise ValueError(f"unknown criteria {bad}")
    if any(not 0 <= v <= 10 for v in s.values()):
        raise ValueError("ratings are 0..10")
    w = sum(WEIGHTS[k] for k in s)
    if w < 50:
        raise ValueError("not enough evidence: rated criteria cover under half the weight")
    return round(sum(s[k] * WEIGHTS[k] for k in s) / w * 10, 1)


def outlier(views, channel_median):
    """How far a video sits above its own channel's normal. 1.0 = typical."""
    return round(views / channel_median, 2) if channel_median else None


def keys(title):
    out = set()
    for w in re.findall(r"[a-z0-9$]+", title.lower()):
        if w in STOP:
            continue
        for suf in ("ing", "ers", "er", "ed", "s"):
            if len(w) > 4 and w.endswith(suf):
                w = w[: -len(suf)]
                break
        out.add(w)
    return out


def similarity(a, b):
    ka, kb = keys(a), keys(b)
    return len(ka & kb) / len(ka | kb) if ka and kb else 0.0


def duplicates(c, title, threshold=0.5):
    rows = c.execute(f"SELECT id,title,status FROM topics WHERE status IN ({','.join('?'*len(BLOCKING))})", BLOCKING).fetchall()
    return [(r["id"], r["title"], r["status"], round(similarity(title, r["title"]), 2)) for r in rows if similarity(title, r["title"]) >= threshold]


def add(c, title, pillar, ratings, source="topic-agent"):
    """Insert a v2-scored idea. A near-copy of a published/scheduled/rejected topic is stored as 'duplicate', never produced."""
    dup = duplicates(c, title)
    status = "duplicate" if dup else "idea"
    c.execute("INSERT INTO topics(title,pillar,model,scores,total,status,source,created_at) VALUES(?,?,?,?,?,?,?,?)",
              (title, pillar, "v2", json.dumps(ratings), score(ratings), status, source, db.now()))
    db.audit(c, "topic-agent", "add", title, f"status={status} dup={dup}")
    return status, dup


def ranked(c, n=10):
    return c.execute("SELECT id,title,pillar,total,model FROM topics WHERE status='idea' ORDER BY total DESC LIMIT ?", (n,)).fetchall()
