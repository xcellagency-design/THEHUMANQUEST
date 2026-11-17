"""SQLite store for the studio. One file, no server: the whole state can be copied or inspected."""
import os, sqlite3, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = os.environ.get("THSQ_DB", os.path.join(ROOT, "studio.db"))

SCHEMA = """
CREATE TABLE IF NOT EXISTS settings(key TEXT PRIMARY KEY, value TEXT);
CREATE TABLE IF NOT EXISTS competitors(id INTEGER PRIMARY KEY, name TEXT UNIQUE, handle TEXT, channel_id TEXT,
  subs INTEGER, total_views INTEGER, videos INTEGER, median_views INTEGER, median_publish_hour_et REAL,
  uploads_sampled INTEGER, notes TEXT, observed_at TEXT);
CREATE TABLE IF NOT EXISTS competitor_videos(video_id TEXT PRIMARY KEY, competitor_id INTEGER, title TEXT,
  published_at TEXT, views INTEGER, outlier REAL, fetched_at TEXT);
CREATE TABLE IF NOT EXISTS topics(id INTEGER PRIMARY KEY, title TEXT, pillar INTEGER, model TEXT, scores TEXT,
  total REAL, status TEXT DEFAULT 'idea', source TEXT, created_at TEXT);
CREATE TABLE IF NOT EXISTS episodes(id TEXT PRIMARY KEY, title TEXT, topic_id INTEGER, status TEXT, created_at TEXT);
CREATE TABLE IF NOT EXISTS facts(id INTEGER PRIMARY KEY, episode_id TEXT, claim TEXT, units TEXT, source TEXT,
  status TEXT, note TEXT, checked_at TEXT);
CREATE TABLE IF NOT EXISTS scripts(id INTEGER PRIMARY KEY, episode_id TEXT, version TEXT, path TEXT, approved INTEGER DEFAULT 0, created_at TEXT);
CREATE TABLE IF NOT EXISTS assets(id INTEGER PRIMARY KEY, episode_id TEXT, kind TEXT, name TEXT, path TEXT,
  unit_from INTEGER, unit_to INTEGER, duration REAL, qc_status TEXT, qc_report TEXT, vidiq_upload_id TEXT, created_at TEXT);
CREATE TABLE IF NOT EXISTS publications(id INTEGER PRIMARY KEY, asset_id INTEGER, platform TEXT, account_id TEXT,
  title TEXT, description TEXT, tags TEXT, category_id INTEGER, privacy TEXT, slot TEXT, publish_at TEXT,
  status TEXT DEFAULT 'queued', vidiq_post_id TEXT, youtube_id TEXT, experiment_id INTEGER, updated_at TEXT);
CREATE TABLE IF NOT EXISTS experiments(id INTEGER PRIMARY KEY, name TEXT, hypothesis TEXT, design TEXT,
  status TEXT, started_at TEXT, result TEXT);
CREATE TABLE IF NOT EXISTS analytics(id INTEGER PRIMARY KEY, youtube_id TEXT, captured_at TEXT, metric TEXT,
  value REAL, window TEXT, source TEXT);
CREATE TABLE IF NOT EXISTS approvals(id INTEGER PRIMARY KEY, at TEXT, mode TEXT, action TEXT, subject TEXT, granted_by TEXT, note TEXT);
CREATE TABLE IF NOT EXISTS jobs(id INTEGER PRIMARY KEY, agent TEXT, subject TEXT, status TEXT, attempts INTEGER DEFAULT 0,
  max_attempts INTEGER DEFAULT 3, last_error TEXT, credits REAL DEFAULT 0, started_at TEXT, finished_at TEXT);
CREATE TABLE IF NOT EXISTS audit(id INTEGER PRIMARY KEY, at TEXT, agent TEXT, action TEXT, subject TEXT, detail TEXT);
"""
DEFAULTS = {"approval_mode": "A", "emergency_stop": "0", "uploads_per_day": "2", "timezone": "America/New_York",
            "youtube_account": "UCuWqWScVJOHZQmXajM2TM-A", "category_id": "27"}


def now():
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def connect(path=None):
    c = sqlite3.connect(path or DB)
    c.row_factory = sqlite3.Row
    c.executescript(SCHEMA)
    for k, v in DEFAULTS.items():
        c.execute("INSERT OR IGNORE INTO settings VALUES(?,?)", (k, v))
    c.commit()
    return c


def get(c, key):
    r = c.execute("SELECT value FROM settings WHERE key=?", (key,)).fetchone()
    return r["value"] if r else None


def put(c, key, value, by="system"):
    c.execute("INSERT INTO settings VALUES(?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value", (key, str(value)))
    audit(c, by, "setting", key, str(value))


def audit(c, agent, action, subject, detail=""):
    c.execute("INSERT INTO audit(at,agent,action,subject,detail) VALUES(?,?,?,?,?)", (now(), agent, action, str(subject), str(detail)))
    c.commit()
