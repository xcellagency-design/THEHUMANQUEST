"""Loads what already exists into the database: launch-plan topics and fact table, competitors, EP001 and its videos.
Safe to re-run: it rebuilds the seeded tables from the sources and leaves settings, approvals and audit alone."""
import glob, json, os, re
from . import db

PLAN = os.path.join(db.ROOT, "docs", "launch_plan.md")
SHORTS = "out/shorts"
ACCOUNT = "UCuWqWScVJOHZQmXajM2TM-A"
TAIL = "\n\nFull episode on the channel.\n\n#shorts #pyramids #ancientegypt #history"
UNITS = ["1,2,29", "28,29", "19,20,21", "17,18", "25,26", "26,27,55,56", "30,31,82,83,84", "33", "34,35", "32,36", "37", "39,40,41,42", "43",
         "45,46,47,48,49,50,51,52", "53", "54", "57", "58,59", "64,65,67,68", "63,66", "75,76,77,79"]
# Re-checks made on 2026-11-17 against sources opened that day. Index = row in the launch-plan fact table.
RECHECK = {8: ("qualified", "Arithmetic on an assumed 23-year build. The narration says 'if'."),
           9: ("qualified", "2.5 t average is widely reported; 'a pickup truck' is an approximate comparison."),
           10: ("verified", "146.6 m original height; tallest structure for 3,800+ years until Lincoln Cathedral, 1311 (Wikipedia: Great Pyramid of Giza; The Collector)."),
           14: ("verified", "First coins: Lydia, late 7th century BC (LBMA; ANA Money Museum). About 1,900 years after 2560 BC."),
           15: ("verified", "Ten loaves and a measure of beer: Tyldesley via Facts and Details; Hilary Wilson, The Past. Beer amount varied."),
           19: ("verified", "Arthritis and damaged lower vertebrae: excavation supervisor quoted by Christian Science Monitor, 2010. Survived amputation: reported by Hawass, secondary source."),
           20: ("verified", "Found 1990 when a tourist's horse stumbled on a wall (CBC/AP 2010; Smithsonian). Beer and bread jars in tombs (AP 2010).")}
LIVE = [("long", "THSQ_EP001_pyramid-builders_v2", "What Was It Actually Like to Build the Pyramids?", "kTbYt5u_aj4", 0, 87, 2),
        ("short", "THSQ_short1", "You Were Lied To About Who Built the Pyramids #shorts", "JcQqfpliW7U", 0, 6, 2),
        ("short", "THSQ_short2", "The Wet Sand Trick That Moved the Pyramids #shorts", "e_ZtVaDCcTI", 38, 44, 176),
        ("short", "THSQ_short4", "Pyramid Builders Were Paid in Beer #shorts", "sRiwYQCOB9w", 53, 60, 21),
        ("short", "THSQ_short5", "The Pyramid Builders Got Medical Care #shorts", "mfIIiMyAxKw", 62, 69, 24),
        ("short", "THSQ_short6", "The Pyramid Builders Signed Their Work #shorts", "sK3_3Z7emlE", 80, 87, 0)]
QUEUE = [("THSQ_short3", 46, 52, "The 4,500-Year-Old Timesheet From the Pyramids #shorts",
          "A boat captain named Merer logged his stone deliveries to the Great Pyramid. It is the oldest inscribed papyrus ever found, and it reads like a timesheet.",
          ["diary of merer", "pyramid builders", "ancient egypt", "great pyramid of giza", "history shorts"]),
         ("THSQ_short7", 14, 21, "Pyramid Builders Couldn't Say No #shorts",
          "Not slaves, not volunteers. When the Nile flooded the fields, the king's men came for the farmers. Historians still argue about how much choice they had.",
          ["pyramid builders", "were the pyramids built by slaves", "ancient egypt", "who built the pyramids", "history shorts"]),
         ("THSQ_short8", 24, 29, "The Lost City Built for the Pyramid Workers #shorts",
          "You expect a camp. You get a city: royal grain silos, bakeries by the dozen, and halls that slept forty or fifty men.",
          ["lost city of the pyramid builders", "pyramid builders", "ancient egypt daily life", "giza", "history shorts"]),
         ("THSQ_short9", 33, 38, "One Pyramid Block Every 2 Minutes #shorts",
          "About 2.3 million blocks. If the build took around 23 years, that is roughly 270 a day, with rope, a sledge and a crew. The build time is an assumption; the rest follows from it.",
          ["how were the pyramids built", "great pyramid of giza", "pyramid builders", "ancient egypt", "history shorts"]),
         ("THSQ_short10", 30, 32, "A Pyramid Crew Called The Drunkards #shorts",
          "Pyramid work gangs had names, and they painted them on the blocks. One was the Friends of Khufu. A later one was the Drunkards of Menkaure.",
          ["pyramid builders", "drunkards of menkaure", "friends of khufu", "ancient egypt", "history shorts"]),
         ("THSQ_short11", 73, 79, "Why Pyramid Builders Were Buried Beside the King #shorts",
          "In 1990 a cemetery turned up beside the pyramids: small tombs, the builders' own, with beer and bread packed for the next world.",
          ["pyramid builders", "tombs of the pyramid builders", "were the pyramids built by slaves", "ancient egypt", "history shorts"]),
         ("THSQ_short12", 7, 13, "You're 17. It's 2560 BC. You Build Pyramids #shorts",
          "You farm barley on the Nile. You are made up; everything that happens to you is in the evidence. Three quests, and a hidden fourth.",
          ["pyramid builders", "ancient egypt daily life", "what was it like", "who built the pyramids", "history shorts"])]
COMP = [("Ink Explainer", "@inkexplainer96", "UCpgrEMx8diLrw7YNQ6r3uUw", 166000, 28900000, 20, 15.8, 21, "16 of 21 recent uploads went out 1-5 PM ET"),
        ("Unknown Frequencies", "@unknownfrequencies-tv", "UCm1yxl_4qMbStLHpHQu6xWg", 86400, 11500000, 23, 14.6, 26, "20 of 26 went out 10 AM-5 PM ET"),
        ("Crayon Capital", "@crayon_capital", "UCP9RPj_BG0vit2TNM7LuRxA", 302000, 25300000, 34, 9.2, 35, "31 of 35 went out before 1 PM ET; likely a non-US uploader")]


def path_of(stem):
    """Path relative to the repo root. Video files are not kept on main, so the file may be absent in a fresh clone."""
    hits = glob.glob(os.path.join(db.ROOT, SHORTS, stem + "_*.mp4")) + glob.glob(os.path.join(db.ROOT, "out", stem + ".mp4"))
    return os.path.relpath(hits[0], db.ROOT) if hits else f"{SHORTS}/{stem}.mp4"


def run(c):
    for t in ("topics", "facts", "competitors", "assets", "publications", "episodes", "experiments", "analytics"):
        c.execute(f"DELETE FROM {t}")
    md = open(PLAN, encoding="utf-8").read()
    for m in re.finditer(r"^\| (\d+) \| (.+?) \| (\d) \| (.+?) \| (\d+) \| (\d+) \| (\d+) \| (\d+) \| (\d+) \| (\d+) \| (\d+) \|$", md, re.M):
        n, title, pillar, anchor, *s = m.groups()
        s = list(map(int, s))
        c.execute("INSERT INTO topics(id,title,pillar,model,scores,total,status,source,created_at) VALUES(?,?,?,?,?,?,?,?,?)",
                  (int(n), title, int(pillar), "v1", json.dumps(dict(zip("DCSOVE", s[:6]), anchor=anchor)), s[6], "published" if n == "1" else "idea", "launch plan", db.now()))
    c.execute("INSERT INTO episodes VALUES('EP001','What Was It Actually Like to Build the Pyramids?',1,'published',?)", (db.now(),))
    table = md.split("### 2. Research and fact table")[1].split("###")[0]
    rows = [r for r in re.findall(r"^\| (.+?) \| (.+?) \| (.+?) \|$", table, re.M) if not r[0].startswith(("Claim", "---"))]
    assert len(rows) == len(UNITS), (len(rows), len(UNITS))
    for i, (claim, src, status) in enumerate(rows):
        st, note = ("verified", status) if status.startswith("Solid") else ("unverified", status)
        if i in RECHECK:
            st, note = RECHECK[i]
        if i == 19:
            claim = "Worn spines and joints; amputations the patient survived"
        c.execute("INSERT INTO facts(episode_id,claim,units,source,status,note,checked_at) VALUES('EP001',?,?,?,?,?,?)", (claim, UNITS[i], src, st, note, db.now()))
    c.execute("INSERT INTO facts(episode_id,claim,units,source,status,note,checked_at) VALUES('EP001',?,?,?,?,?,?)",
              ("Most people in the builders' cemetery died in their thirties", "70", "Facts and Details, Ancient Origins", "unverified",
               "No primary source opened. Line is in the published long episode only, not in any Short.", db.now()))
    for name, handle, cid, subs, views, n, hour, sampled, note in COMP:
        c.execute("INSERT INTO competitors(name,handle,channel_id,subs,total_views,videos,median_publish_hour_et,uploads_sampled,notes,observed_at) VALUES(?,?,?,?,?,?,?,?,?,?)",
                  (name, handle, cid, subs, views, n, hour, sampled, note, "2026-11-17"))
    design = {"slots": {"A": "09:00", "B": "12:00", "C": "15:00", "D": "19:00"}, "timezone": "America/New_York", "pairs": [["B", "D"], ["A", "C"]],
              "days": 14, "metric": "views_d0_d7", "unit": "one Short", "rule": {"min_n": 7, "min_lift": 0.30, "alpha": 0.10}, "baseline": ["B", "D"]}
    c.execute("INSERT INTO experiments(id,name,hypothesis,design,status,started_at) VALUES(1,?,?,?,?,?)",
              ("Upload time test 1", "Publish slot changes first-week views of a Short by 30% or more", json.dumps(design), "planned", None))
    for kind, stem, title, yt, a, b, views in LIVE:
        cur = c.execute("INSERT INTO assets(episode_id,kind,name,path,unit_from,unit_to,created_at) VALUES('EP001',?,?,?,?,?,?)", (kind, stem, path_of(stem), a, b, db.now()))
        c.execute("INSERT INTO publications(asset_id,platform,account_id,title,privacy,status,publish_at,youtube_id,category_id,updated_at) VALUES(?,?,?,?,?,?,?,?,27,?)",
                  (cur.lastrowid, "YOUTUBE", ACCOUNT, title, "public", "live", "2026-11-17T00:56:00-05:00", yt, db.now()))
        c.execute("INSERT INTO analytics(youtube_id,captured_at,metric,value,window,source) VALUES(?,?,?,?,?,?)", (yt, "2026-11-17T06:15:00Z", "views", views, "first 20 minutes", "vidiq_user_videos"))
    for stem, a, b, title, desc, tags in QUEUE:
        cur = c.execute("INSERT INTO assets(episode_id,kind,name,path,unit_from,unit_to,created_at) VALUES('EP001','short',?,?,?,?,?)", (stem, path_of(stem), a, b, db.now()))
        c.execute("INSERT INTO publications(asset_id,platform,account_id,title,description,tags,category_id,privacy,status,experiment_id,updated_at) VALUES(?,?,?,?,?,?,27,'public','queued',1,?)",
                  (cur.lastrowid, "YOUTUBE", ACCOUNT, title, desc + TAIL, json.dumps(tags), db.now()))
    c.commit()
    db.audit(c, "seed", "load", "launch plan + EP001", f"topics={c.execute('SELECT COUNT(*) FROM topics').fetchone()[0]} facts={len(rows)+1}")
