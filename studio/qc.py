"""Automated checks on a finished video file. Measures; does not judge taste.

fail  = must go back to production (wrong format, missing/short audio, black video, loudness far off, speech unrecognisable)
warn  = a human should look (long static hold, silence, loudness slightly off, captions drifting)
A pass here is necessary, not sufficient: a person still watches the video before it is approved.
"""
import json, os, re, subprocess, difflib, statistics as st

SPEC = {"short": {"w": 1080, "h": 1920, "min": 8, "max": 180}, "long": {"w": 1920, "h": 1080, "min": 60, "max": 3600}}
LUFS_TARGET, TP_MAX = -16.0, -1.0


def _run(a):
    p = subprocess.run(a, capture_output=True, text=True)
    return p.stdout + p.stderr


def measure(path):
    info = json.loads(subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", path], capture_output=True, text=True).stdout or "{}")
    v = next((s for s in info.get("streams", []) if s["codec_type"] == "video"), None)
    a = next((s for s in info.get("streams", []) if s["codec_type"] == "audio"), None)
    m = {"has_video": bool(v), "has_audio": bool(a), "duration": float(info.get("format", {}).get("duration", 0))}
    if v:
        m.update(width=v["width"], height=v["height"], fps=round(eval(v["r_frame_rate"]), 2), v_dur=float(v.get("duration", m["duration"])))
    if a:
        m["a_dur"] = float(a.get("duration", m["duration"]))
    af = ["-af", "silencedetect=n=-45dB:d=1.5,ebur128=peak=true"] if a else ["-an"]
    log = _run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-vf", "blackdetect=d=0.4:pix_th=0.08,freezedetect=n=-55dB:d=5", *af, "-f", "null", "-"])
    m["black"] = [(float(x), float(y)) for x, y in re.findall(r"black_start:([\d.]+) black_end:([\d.]+)", log)]
    fs = [float(x) for x in re.findall(r"freeze_start: ([\d.]+)", log)]
    fd = [float(x) for x in re.findall(r"freeze_duration: ([\d.]+)", log)]
    m["freeze"] = list(zip(fs, fd))
    m["silence"] = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", log)]
    tail = log[log.rfind("Summary:"):] if "Summary:" in log else ""
    i = re.search(r"I:\s+(-?[\d.]+) LUFS", tail)
    p = re.search(r"Peak:\s+(-?[\d.]+) dBFS", tail)
    m["lufs"] = float(i.group(1)) if i else None
    m["true_peak"] = float(p.group(1)) if p else None
    return m


def speech(path, words):
    """Transcribe and compare with the intended words [(word, start, end)]. Returns similarity 0..1 and caption drift in seconds."""
    import numpy as np
    from scipy.io import wavfile
    from faster_whisper import WhisperModel
    wav = path + ".qc.wav"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", path, "-ac", "1", "-ar", "16000", wav], check=True)
    sr, x = wavfile.read(wav)
    os.remove(wav)
    segs, _ = WhisperModel("base.en", compute_type="int8").transcribe(x.astype(np.float32) / 32768, word_timestamps=True)
    norm = lambda w: re.sub(r"[^a-z0-9]", "", w.lower())
    heard = [(norm(w.word), w.start) for s in segs for w in s.words if norm(w.word)]
    want = [(norm(w), s) for w, s, e in words if norm(w)]
    sm = difflib.SequenceMatcher(None, [w for w, _ in want], [w for w, _ in heard], autojunk=False)
    drift = [abs(want[b.a + k][1] - heard[b.b + k][1]) for b in sm.get_matching_blocks() for k in range(b.size)]
    blocks = [b for b in sm.get_matching_blocks() if b.size]
    extra = len(heard) - (blocks[-1].b + blocks[-1].size) if blocks else 0
    return {"similarity": round(sm.ratio(), 3), "extra_words_at_end": extra, "caption_drift_median": round(st.median(drift), 3) if drift else None,
            "caption_drift_p90": round(sorted(drift)[int(len(drift) * 0.9)], 3) if drift else None, "heard": " ".join(w for w, _ in heard)}


def check(path, kind, words=None):
    spec, m, fail, warn = SPEC[kind], measure(path), [], []
    if not m["has_video"]: fail.append("no video stream")
    if not m["has_audio"]: fail.append("no audio stream")
    if m["has_video"] and (m["width"], m["height"]) != (spec["w"], spec["h"]): fail.append(f"resolution {m.get('width')}x{m.get('height')}, want {spec['w']}x{spec['h']}")
    if not spec["min"] <= m["duration"] <= spec["max"]: fail.append(f"duration {m['duration']:.1f}s outside {spec['min']}-{spec['max']}s")
    if m["has_audio"] and m["has_video"] and abs(m["a_dur"] - m["v_dur"]) > 0.5: fail.append(f"audio/video length differ by {abs(m['a_dur']-m['v_dur']):.2f}s")
    black = sum(e - s for s, e in m["black"])
    if black >= 1.5: fail.append(f"{black:.1f}s of black video")
    elif black > 0: warn.append(f"{black:.1f}s of black video")
    if m["lufs"] is None and m["has_audio"]: fail.append("loudness could not be measured")
    elif m["has_audio"]:
        if abs(m["lufs"] - LUFS_TARGET) > 3: fail.append(f"loudness {m['lufs']} LUFS, target {LUFS_TARGET}")
        elif abs(m["lufs"] - LUFS_TARGET) > 1.5: warn.append(f"loudness {m['lufs']} LUFS, target {LUFS_TARGET}")
        if m["true_peak"] is not None and m["true_peak"] > -0.3: fail.append(f"true peak {m['true_peak']} dBFS (clipping risk)")
        elif m["true_peak"] is not None and m["true_peak"] > TP_MAX: warn.append(f"true peak {m['true_peak']} dBFS, want under {TP_MAX}")
    for s, d in m["freeze"]: warn.append(f"picture static for {d:.1f}s from {s:.1f}s")
    for s in m["silence"]:
        if s < m["duration"] - 2: warn.append(f"silence from {s:.1f}s")
    if words:
        try:
            sp = speech(path, words); m["speech"] = sp
            if sp["similarity"] < 0.6: fail.append(f"speech matches script only {sp['similarity']:.0%}")
            elif sp["similarity"] < 0.85: warn.append(f"speech matches script {sp['similarity']:.0%}")
            if sp["extra_words_at_end"] > 0: warn.append(f"{sp['extra_words_at_end']} spoken word(s) after the script ends (next line leaking in)")
            if sp["caption_drift_median"] is not None and sp["caption_drift_median"] > 0.35: warn.append(f"captions drift {sp['caption_drift_median']}s (median)")
        except Exception as e:  # the speech check is optional; say so instead of passing silently
            warn.append(f"speech check not run: {type(e).__name__}: {e}")
    return {"file": os.path.basename(path), "kind": kind, "status": "fail" if fail else "warn" if warn else "pass", "fail": fail, "warn": warn, "measured": m}
