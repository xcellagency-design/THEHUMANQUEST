"""Build one long-form episode from engine/<module>.py, start to finish.

    python3 engine/build.py ep02 EP002 some-slug            full build -> out/THSQ_EP002_some-slug.mp4
    python3 engine/build.py ep01 EP001 smoke --smoke        first 6 narration lines only (pipeline check, a few minutes)

Steps: stills + contact sheets -> narration (Kokoro) -> timing + audio mix -> motion test on every still ->
motion render -> encode with loudness normalised to -16 LUFS. Stops at the first failing step.
Look at work/<EP>/sheet*.jpg before trusting the result: the code cannot tell whether a drawing reads well.
"""
import json, os, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def main():
    mod, epid, slug = sys.argv[1:4]
    smoke = "--smoke" in sys.argv
    work = os.path.join(ROOT, "work", epid + ("_smoke" if smoke else ""))
    out_dir = os.environ.get("THSQ_OUT", os.path.join(ROOT, "out"))
    for d in ("frames", "audio", "seg"):
        os.makedirs(os.path.join(work, d), exist_ok=True)
    os.makedirs(out_dir, exist_ok=True)
    if not os.path.exists(os.path.join(work, "models")):
        os.symlink(os.path.join(HERE, "models"), os.path.join(work, "models"))
    env = dict(os.environ, THSQ_EP=mod, PYTHONPATH=HERE)
    if smoke:
        env["THSQ_UNITS"] = "6"

    def run(*a, capture=False):
        print(">>", *a, flush=True)
        return subprocess.run([sys.executable, os.path.join(HERE, a[0]), *a[1:]], cwd=work, env=env, check=True, capture_output=capture, text=True)

    run("render.py")
    run("tts.py")
    run("assemble.py")
    t = run("render2.py", "test", capture=True).stdout
    print(t[-400:])
    if "errors: 0" not in t:
        sys.exit("motion test failed: fix the scenes listed above")
    run("render2.py", "2")
    dur = json.load(open(os.path.join(work, "timing.json")))["total"]
    kbps = int(min(2600, 90e6 * 8 / dur / 1000 - 170))  # keeps the file under ~90 MB so it can be hosted in git
    out = os.path.join(out_dir, f"THSQ_{epid}_{slug}.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "segs.txt", "-i", "mix.wav", "-vf", "hqdn3d=2:1.5:3:3",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "23", "-maxrate", f"{kbps}k", "-bufsize", f"{2*kbps}k", "-pix_fmt", "yuv420p",
                    "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "48000", "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", out], cwd=work, check=True)
    if not smoke:
        keep = os.path.join(ROOT, "03_episodes", epid, "work")
        os.makedirs(keep, exist_ok=True)
        for f in ("shotlist.csv", "durations.json", "frames.json", "timing.json"):
            shutil.copy(os.path.join(work, f), keep)
    print("built", out, f"{dur:.1f}s", f"{os.path.getsize(out)/1e6:.1f} MB")


if __name__ == "__main__":
    main()
