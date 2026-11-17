import json, os, subprocess, sys, random
from datetime import date, datetime, timedelta
import pytest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from studio import db, topics, schedule, timing, qc


@pytest.fixture
def c(tmp_path):
    return db.connect(str(tmp_path / "t.db"))


def test_score_weights_and_missing_evidence():
    assert topics.score({k: 10 for k in topics.WEIGHTS}) == 100.0
    assert topics.score({"demand": 8, "story": 8, "novelty": 8, "outperformance": 8, "evergreen": 8}) == 80.0  # re-normalised, not penalised
    with pytest.raises(ValueError): topics.score({"demand": 10, "cost": 10})  # under half the weight rated
    with pytest.raises(ValueError): topics.score({"hype": 9})


def test_duplicate_topic_is_blocked(c):
    c.execute("INSERT INTO topics(title,status) VALUES('What Was It Actually Like to Build the Pyramids?','published')")
    r = {"demand": 9, "story": 9, "novelty": 5, "outperformance": 8, "evergreen": 9}
    assert topics.add(c, "What Was It Really Like Building the Pyramids", 1, r)[0] == "duplicate"
    assert topics.add(c, "What Did a Roman Soldier Actually Eat?", 1, r)[0] == "idea"
    assert topics.outlier(18_600_000, 600_000) == 31.0


def test_rotation_is_balanced():
    p = schedule.plan(date(2026, 11, 17), 14)
    assert len(p) == 28
    assert all(sum(x["slot"] == s for x in p) == 7 for s in "ABCD")
    seen = {}
    for x in p: seen.setdefault(date.fromisoformat(x["date"]).weekday(), set()).add(x["slot"])
    assert all(v == set("ABCD") for v in seen.values())  # every weekday gets both pairs
    assert all(datetime.fromisoformat(x["publish_at"]).utcoffset() == timedelta(hours=-5) for x in p)


def test_past_slots_are_skipped():
    after = datetime(2026, 11, 17, 11, 30, tzinfo=schedule.ET)
    p = schedule.plan(date(2026, 11, 17), 1, after)
    assert [x["slot"] for x in p] == ["D"]  # noon is inside the 45-minute lead, so only 7 PM remains


def _pub(c, qc_status="pass", upload="11111111-1111-4111-8111-111111111111"):
    c.execute("INSERT INTO assets(id,episode_id,kind,name,unit_from,unit_to,qc_status,vidiq_upload_id) VALUES(1,'EP001','short','s',10,20,?,?)", (qc_status, upload))
    t = (datetime.now(schedule.ET) + timedelta(days=1)).isoformat()
    c.execute("INSERT INTO publications(id,asset_id,platform,account_id,title,description,tags,category_id,privacy,publish_at,experiment_id) VALUES(1,1,'YOUTUBE','UCx','T','D','[]',27,'public',?,1)", (t,))
    c.commit()


def test_gates(c):
    _pub(c)
    req = schedule.draft_request(c, 1)
    assert req["destinations"][0]["publishAt"] and req["media"][0]["type"] == "video"
    with pytest.raises(schedule.Blocked, match="no approval"): schedule.may_publish(c, 1)  # drafting is not approval
    schedule.approve(c, "A", "publish", "batch:1", "owner")
    assert schedule.may_publish(c, 1)
    c.execute("INSERT INTO facts(episode_id,claim,units,status) VALUES('EP001','x','15','unverified')"); c.commit()
    with pytest.raises(schedule.Blocked, match="unverified"): schedule.draft_request(c, 1)
    c.execute("UPDATE facts SET units='70'"); c.commit()
    assert schedule.draft_request(c, 1)  # claim is outside this clip
    db.put(c, "emergency_stop", "1")
    with pytest.raises(schedule.Blocked, match="stop"): schedule.may_publish(c, 1)


def test_gate_qc_and_upload(c):
    _pub(c, qc_status="fail")
    with pytest.raises(schedule.Blocked, match="QC"): schedule.draft_request(c, 1)
    c.execute("UPDATE assets SET qc_status='pass', vidiq_upload_id=NULL"); c.commit()
    with pytest.raises(schedule.Blocked, match="library"): schedule.draft_request(c, 1)


def test_timing_rule():
    rng = random.Random(1)
    noise = [(s, rng.lognormvariate(5, 1)) for s in "ABCD" for _ in range(7)]
    assert timing.analyze(noise)["decision"] == "keep_baseline"
    assert timing.analyze(noise[:20])["decision"] == "extend"
    clear = [(s, rng.uniform(90, 110) * (4 if s == "C" else 1)) for s in "ABCD" for _ in range(7)]
    r = timing.analyze(clear)
    assert r["decision"] == "adopt" and r["best"] == "C" and r["p_value"] < 0.01
    base_wins = [(s, rng.uniform(90, 110) * (4 if s == "D" else 1)) for s in "ABCD" for _ in range(7)]
    assert timing.analyze(base_wins)["decision"] == "keep_baseline"


def test_qc_catches_bad_file(tmp_path):
    bad = str(tmp_path / "bad.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "color=black:s=1280x720:r=30:d=10", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-t", "10", "-pix_fmt", "yuv420p", bad], check=True)
    r = qc.check(bad, "short")
    assert r["status"] == "fail" and any("resolution" in f for f in r["fail"]) and any("black" in f for f in r["fail"]) and any("loudness" in f for f in r["fail"])


def test_qc_real_short():
    f = "" + os.path.join(db.ROOT, "out/shorts/THSQ_short10_team-drunkards.mp4") + ""
    if not os.path.exists(f): pytest.skip("render not present")
    r = qc.check(f, "short")
    assert r["status"] in ("pass", "warn") and r["measured"]["width"] == 1080 and not r["fail"]


def test_long_episode_is_planned_before_its_shorts(c):
    for i, kind in enumerate(["short", "short", "long", "short"], 1):
        c.execute("INSERT INTO assets(id,episode_id,kind,name) VALUES(?,?,?,?)", (i, "EP009", kind, f"v{i}"))
        c.execute("INSERT INTO publications(id,asset_id,status) VALUES(?,?,'queued')", (i, i))
    c.commit()
    for seed in range(5):
        c.execute("UPDATE publications SET publish_at=NULL, slot=NULL"); c.commit()
        done, _ = schedule.assign(c, date(2026, 11, 19), datetime(2026, 11, 18, 0, 0, tzinfo=schedule.ET), shuffle_seed=seed)
        assert min(done, key=lambda x: x[2])[0] == 3  # the long video holds the earliest slot of the batch
