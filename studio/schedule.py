"""Publishing calendar and the upload-time experiment rotation.

Two uploads a day. Four candidate slots (Eastern time). Days alternate between two pairs, so over 14 days
every slot is used 7 times and every weekday sees each pair exactly once (7 is odd, so the alternation flips
each week). That keeps day-of-week from masquerading as a time-of-day effect.

This module never talks to YouTube. It produces the exact draft request for the vidIQ publishing tool and
refuses to produce one when a gate is closed. Publishing itself is done by the operator session, and only
after the approval the current mode requires is on record.
"""
import json
from datetime import datetime, date, timedelta
from zoneinfo import ZoneInfo
from . import db

ET = ZoneInfo("America/New_York")
SLOTS = {"A": "09:00", "B": "12:00", "C": "15:00", "D": "19:00"}
PAIRS = [("B", "D"), ("A", "C")]  # pair 0 = the 12 PM / 7 PM baseline from the original brief
MIN_LEAD = timedelta(minutes=45)
EPOCH = date(2026, 11, 17)  # first day of the rotation: a 12 PM + 7 PM day


class Blocked(Exception):
    pass


def plan(start: date, days: int, after: datetime = None, first_pair=0):
    """All slots from start for `days` days, skipping any that fall before after+lead."""
    out = []
    for i in range(days):
        d = start + timedelta(days=i)
        for s in PAIRS[((d - EPOCH).days + first_pair) % 2]:  # parity is tied to the calendar, not to the day planning starts
            h, m = map(int, SLOTS[s].split(":"))
            t = datetime(d.year, d.month, d.day, h, m, tzinfo=ET)
            if after is None or t >= after + MIN_LEAD:
                out.append({"date": d.isoformat(), "slot": s, "publish_at": t.isoformat()})
    return out


def assign(c, start: date, after: datetime, days=14, experiment_id=None, shuffle_seed=None):
    """Give every queued publication the next free slot, oldest first. Empty slots stay empty: no filler."""
    taken = {r["publish_at"] for r in c.execute("SELECT publish_at FROM publications WHERE status IN ('queued','drafted','scheduled','live') AND publish_at IS NOT NULL")}
    free = [p for p in plan(start, days, after) if p["publish_at"] not in taken]
    q = c.execute("SELECT p.id, a.kind, a.episode_id FROM publications p JOIN assets a ON a.id=p.asset_id WHERE p.status='queued' AND p.publish_at IS NULL ORDER BY p.id").fetchall()
    if shuffle_seed is not None:  # random assignment of videos to slots, so a strong video is not always in the same slot
        import random
        random.Random(shuffle_seed).shuffle(q)
    # one episode's videos never run back to back while another episode has something waiting
    groups = {}
    for r in q:
        groups.setdefault(r["episode_id"], []).append(r)
    # the long episode goes out before the Shorts cut from it, so "full episode on the channel" is true when a Short says it
    for g in groups.values():
        g.sort(key=lambda r: r["kind"] != "long")
    q = [g[i] for i in range(max(map(len, groups.values()), default=0)) for g in groups.values() if i < len(g)]
    done = []
    for row, p in zip(q, free):
        c.execute("UPDATE publications SET slot=?, publish_at=?, experiment_id=?, updated_at=? WHERE id=?", (p["slot"], p["publish_at"], experiment_id if row["kind"] == "short" else None, db.now(), row["id"]))
        done.append((row["id"], p["slot"], p["publish_at"]))
    c.commit()
    return done, free[len(q):]


def gate(c, pub_id):
    """Everything that must be true before a draft request may be built."""
    if db.get(c, "emergency_stop") == "1":
        raise Blocked("emergency stop is on")
    p = c.execute("SELECT p.*, a.qc_status, a.vidiq_upload_id, a.episode_id, a.unit_from, a.unit_to, a.name FROM publications p JOIN assets a ON a.id=p.asset_id WHERE p.id=?", (pub_id,)).fetchone()
    if p is None:
        raise Blocked("no such publication")
    if p["qc_status"] not in ("pass", "warn"):
        raise Blocked(f"{p['name']}: QC is {p['qc_status']}")
    if not p["vidiq_upload_id"]:
        raise Blocked(f"{p['name']}: video is not in the vidIQ library yet")
    if not p["publish_at"] or datetime.fromisoformat(p["publish_at"]) < datetime.now(ET) + timedelta(minutes=5):
        raise Blocked(f"{p['name']}: no future publish time")
    for f in c.execute("SELECT claim, units FROM facts WHERE episode_id=? AND status='unverified'", (p["episode_id"],)):
        us = {int(x) for x in (f["units"] or "").split(",") if x}
        if p["unit_from"] is None or any(p["unit_from"] <= u <= p["unit_to"] for u in us):
            raise Blocked(f"{p['name']}: unverified claim in narration: {f['claim'][:60]}")
    return p


def draft_request(c, pub_id):
    """Arguments for vidiq_social_post_draft_create. Drafting posts nothing."""
    p = gate(c, pub_id)
    return {"media": [{"type": "video", "id": p["vidiq_upload_id"]}],
            "destinations": [{"platform": "YOUTUBE", "platformAccountId": p["account_id"], "title": p["title"], "text": p["description"],
                              "tags": json.loads(p["tags"] or "[]"), "categoryId": p["category_id"], "privacyStatus": p["privacy"], "publishAt": p["publish_at"]}]}


def may_publish(c, pub_id):
    """Mode A: a recorded approval naming this publication (or its batch). B: QC pass plus a recorded policy approval.
    C: a recorded unattended authorisation. The stop switch beats all three."""
    p = gate(c, pub_id)
    mode = db.get(c, "approval_mode")
    want = {"A": ("publish", (f"pub:{pub_id}", f"batch:{p['experiment_id']}")), "B": ("policy", ("queue",)), "C": ("unattended", ("all",))}[mode]
    ok = c.execute(f"SELECT 1 FROM approvals WHERE mode=? AND action=? AND subject IN ({','.join('?'*len(want[1]))})", (mode, want[0], *want[1])).fetchone()
    if not ok:
        raise Blocked(f"mode {mode}: no approval on record for publication {pub_id}")
    return True


def approve(c, mode, action, subject, granted_by, note=""):
    c.execute("INSERT INTO approvals(at,mode,action,subject,granted_by,note) VALUES(?,?,?,?,?,?)", (db.now(), mode, action, subject, granted_by, note))
    db.audit(c, "approval", action, subject, f"mode={mode} by={granted_by} {note}")
