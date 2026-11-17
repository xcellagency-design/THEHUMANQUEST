"""python3 -m studio.cli <command>      (run from the repo root)

State
  status                         counts, queue, anything blocked
  report                         performance digest: every live video, slot medians, runway, next topics
  seed                           rebuild the database from docs/launch_plan.md + EP001 (first setup only)
Planning
  topic-next [N]                 best unproduced ideas
  topic-start ID EPnnn           mark an idea in production and open the episode
  topic-add PILLAR 'Title' '{"demand":8,...}'   score and store a new idea (duplicates are refused)
Production
  register PACKAGE.json          add an episode's long video, Shorts, facts and publish texts to the queue
  qc [NAME...]                   automated QC on videos present on disk
  plan YYYY-MM-DD [HH:MM]        give queued videos the next free slots (ET)
Publishing
  uploaded NAME UPLOAD_ID        the video is in the vidIQ library
  drafts                         draft request for every planned video, or the reason it is blocked
  drafted PUB POST_ID            a vidIQ draft exists
  carried                        drafts and refused uploads from earlier runs, with the arguments to re-send before publishing
  approve PUB...                 the owner approved these publications (records who and when)
  scheduled PUB | live PUB YOUTUBE_ID | failed PUB 'why'
Measuring
  snapshot YOUTUBE_ID METRIC VALUE [WINDOW]     e.g. snapshot abc123 views_d0_d7 412
  timing                         upload-time experiment verdict
Control
  stop | resume | mode A|B|C
"""
import json, os, statistics as st, sys
from datetime import date, datetime
from . import db, qc, schedule, seed, timing, topics


def status(c):
    print("mode", db.get(c, "approval_mode"), "| stop", db.get(c, "emergency_stop"), "| uploads/day", db.get(c, "uploads_per_day"))
    print("facts:", dict(c.execute("SELECT status, COUNT(*) FROM facts GROUP BY status").fetchall()))
    print("publications:", dict(c.execute("SELECT status, COUNT(*) FROM publications GROUP BY status").fetchall()))
    for r in c.execute("SELECT p.id,a.name,a.kind,a.qc_status,p.slot,p.publish_at,p.status,a.vidiq_upload_id IS NOT NULL up FROM publications p JOIN assets a ON a.id=p.asset_id WHERE p.status NOT IN ('live') ORDER BY p.publish_at IS NULL, p.publish_at, p.id"):
        print("  ", tuple(r))


def report(c):
    print("== live videos ==")
    for p in c.execute("SELECT p.youtube_id,p.title,p.slot,p.publish_at,a.kind FROM publications p JOIN assets a ON a.id=p.asset_id WHERE p.status='live' ORDER BY p.publish_at"):
        m = {r["metric"]: (r["value"], r["captured_at"][:16]) for r in c.execute("SELECT metric,value,captured_at FROM analytics WHERE youtube_id=? ORDER BY captured_at", (p["youtube_id"],))}
        print(f"{p['kind']:5} {p['slot'] or '-'} {(p['publish_at'] or '')[:16]} {p['title'][:52]:52}", {k: v[0] for k, v in m.items()})
    print("== timing test ==")
    print(json.dumps(timing.analyze(timing.rows_from_db(c, 1)))[:600])
    nxt = c.execute("SELECT COUNT(*) n, MAX(publish_at) last FROM publications WHERE status IN ('queued','drafted','scheduled') AND publish_at IS NOT NULL").fetchone()
    print("== runway ==", nxt["n"], "videos planned, last slot", nxt["last"], "| unplanned in queue:", c.execute("SELECT COUNT(*) FROM publications WHERE status='queued' AND publish_at IS NULL").fetchone()[0])
    print("== unverified facts ==", [r[0][:70] for r in c.execute("SELECT claim FROM facts WHERE status='unverified'")])
    print("== next topics ==")
    for r in topics.ranked(c, 5): print("  ", tuple(r))


def register(c, path):
    pk = json.load(open(path)); ep = pk["episode"]; acct = db.get(c, "youtube_account")
    c.execute("INSERT OR REPLACE INTO episodes VALUES(?,?,?,?,?)", (ep, pk["title"], pk.get("topic_id"), "produced", db.now()))
    for f in pk.get("facts", []):
        c.execute("INSERT INTO facts(episode_id,claim,units,source,status,note,checked_at) VALUES(?,?,?,?,?,?,?)", (ep, f["claim"], f.get("units", ""), f["source"], f["status"], f.get("note", ""), db.now()))
    items = [("long", pk["long"], None)] + [("short", s, s["units"]) for s in pk.get("shorts", [])]
    for kind, v, units in items:
        name = os.path.basename(v["file"])[:-4]
        a, b = units if units else (0, 10 ** 6)
        cur = c.execute("INSERT INTO assets(episode_id,kind,name,path,unit_from,unit_to,created_at) VALUES(?,?,?,?,?,?,?)", (ep, kind, name, v["file"], a, b, db.now()))
        c.execute("INSERT INTO publications(asset_id,platform,account_id,title,description,tags,category_id,privacy,status,updated_at) VALUES(?,?,?,?,?,?,?,?,?,?)",
                  (cur.lastrowid, "YOUTUBE", acct, v["title"], v["description"], json.dumps(v.get("tags", [])), int(db.get(c, "category_id")), "public", "queued", db.now()))
    if pk.get("topic_id"): c.execute("UPDATE topics SET status='published' WHERE id=?", (pk["topic_id"],))
    c.commit(); db.audit(c, "production", "register", ep, f"{len(items)} videos, {len(pk.get('facts', []))} facts")
    print("registered", ep, len(items), "videos")


def run_qc(c, names):
    for a in c.execute("SELECT * FROM assets ORDER BY id").fetchall():
        f = os.path.join(db.ROOT, a["path"])
        if (names and a["name"] not in names) or not os.path.exists(f):
            continue
        words = json.load(open(f[:-4] + ".words.json")) if os.path.exists(f[:-4] + ".words.json") else None
        r = qc.check(f, a["kind"], words)
        d = os.path.join(db.ROOT, "03_episodes", a["episode_id"], "10_qc"); os.makedirs(d, exist_ok=True)
        out = os.path.join(d, a["name"] + ".qc.json"); json.dump(r, open(out, "w"), indent=1)
        c.execute("UPDATE assets SET qc_status=?, qc_report=?, duration=? WHERE id=?", (r["status"], os.path.relpath(out, db.ROOT), r["measured"]["duration"], a["id"])); c.commit()
        sp = r["measured"].get("speech", {})
        print(f"{a['name'][:44]:44} {r['status']:5} {r['measured']['duration']:6.1f}s {r['measured']['lufs']} LUFS tp {r['measured']['true_peak']} speech {sp.get('similarity')} drift {sp.get('caption_drift_median')}", r["fail"] + r["warn"], flush=True)


def setpub(c, pub, status, **kw):
    sets = ", ".join(f"{k}=?" for k in kw); sets = (", " + sets) if sets else ""
    c.execute(f"UPDATE publications SET status=?, updated_at=?{sets} WHERE id=?", (status, db.now(), *kw.values(), int(pub))); c.commit()
    db.audit(c, "publishing", status, f"pub:{pub}", json.dumps(kw)); print("pub", pub, "->", status)


def main(argv):
    c = db.connect(); cmd = argv[0] if argv else "status"; a = argv[1:]
    if cmd == "seed": seed.run(c); status(c)
    elif cmd == "status": status(c)
    elif cmd == "report": report(c)
    elif cmd == "topic-next":
        for r in topics.ranked(c, int(a[0]) if a else 5): print(tuple(r))
    elif cmd == "topic-start":
        c.execute("UPDATE topics SET status='in_production' WHERE id=?", (int(a[0]),))
        t = c.execute("SELECT title FROM topics WHERE id=?", (int(a[0]),)).fetchone()["title"]
        c.execute("INSERT OR REPLACE INTO episodes VALUES(?,?,?,?,?)", (a[1], t, int(a[0]), "in_production", db.now())); c.commit(); print(a[1], t)
    elif cmd == "topic-add": print(topics.add(c, a[1], int(a[0]), json.loads(a[2])))
    elif cmd == "register": register(c, a[0])
    elif cmd == "qc": run_qc(c, set(a))
    elif cmd == "plan":
        d = date.fromisoformat(a[0]); after = datetime.now(schedule.ET)
        if len(a) > 1:
            h, m = map(int, a[1].split(":")); after = max(after, datetime(d.year, d.month, d.day, h, m, tzinfo=schedule.ET) - schedule.MIN_LEAD)
        done, empty = schedule.assign(c, d, after, experiment_id=1, shuffle_seed=int(d.strftime("%Y%m%d")))
        for x in done: print("planned", x)
        print("first empty slots:", [(e["date"], e["slot"]) for e in empty[:4]])
    elif cmd == "uploaded":
        c.execute("UPDATE assets SET vidiq_upload_id=? WHERE name=?", (a[1], a[0])); c.commit(); db.audit(c, "publishing", "uploaded", a[0], a[1]); print("ok")
    elif cmd == "drafts":
        for r in c.execute("SELECT id FROM publications WHERE status='queued' AND publish_at IS NOT NULL ORDER BY publish_at").fetchall():
            try: print(json.dumps({"pub": r["id"], **schedule.draft_request(c, r["id"])}))
            except schedule.Blocked as e: print(f"pub {r['id']} BLOCKED: {e}")
    elif cmd == "carried":  # drafts and refused uploads left by an earlier run: the arguments to re-send with vidiq_social_post_draft_update before publishing
        for r in c.execute("SELECT p.id, p.status, p.vidiq_post_id, a.kind, a.episode_id FROM publications p JOIN assets a ON a.id=p.asset_id WHERE p.status IN ('drafted','failed') AND p.vidiq_post_id IS NOT NULL ORDER BY p.publish_at").fetchall():
            try:
                req = schedule.draft_request(c, r["id"]); pk = os.path.join(db.ROOT, "03_episodes", r["episode_id"], "09_package", "package.json")
                thumb = json.load(open(pk)).get("long", {}).get("thumbnail_image_id") if r["kind"] == "long" and os.path.exists(pk) else None
                if thumb: req["destinations"][0]["thumbnailImageId"] = thumb
                print(json.dumps({"pub": r["id"], "status": r["status"], "postId": r["vidiq_post_id"], "destinations": req["destinations"]}))
            except schedule.Blocked as e: print(f"pub {r['id']} BLOCKED: {e}")
    elif cmd == "drafted": setpub(c, a[0], "drafted", vidiq_post_id=a[1])
    elif cmd == "approve":
        for p in a: schedule.approve(c, db.get(c, "approval_mode"), "publish", f"pub:{p}", "owner", "approved in chat")
        print("approved", a)
    elif cmd == "scheduled": schedule.may_publish(c, int(a[0])); setpub(c, a[0], "scheduled")
    elif cmd == "live": setpub(c, a[0], "live", youtube_id=a[1])
    elif cmd == "failed": setpub(c, a[0], "failed"); db.audit(c, "publishing", "failure", f"pub:{a[0]}", a[1] if len(a) > 1 else "")
    elif cmd == "snapshot":
        c.execute("INSERT INTO analytics(youtube_id,captured_at,metric,value,window,source) VALUES(?,?,?,?,?,?)", (a[0], db.now(), a[1], float(a[2]), a[3] if len(a) > 3 else "", "vidiq")); c.commit(); print("ok")
    elif cmd == "timing": print(json.dumps(timing.analyze(timing.rows_from_db(c, 1)), indent=1))
    elif cmd in ("stop", "resume"): db.put(c, "emergency_stop", "1" if cmd == "stop" else "0", by="operator"); print("emergency_stop =", db.get(c, "emergency_stop"))
    elif cmd == "mode" and a and a[0] in "ABC": db.put(c, "approval_mode", a[0], by="operator"); print("mode =", a[0])
    else: print(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
