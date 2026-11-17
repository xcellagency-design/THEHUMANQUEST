# The Human Side Quest: studio
Code-generated YouTube channel. `CLAUDE.md` is the operating manual; start there.

    bash setup.sh
    python3 -m studio.cli            # all commands
    python3 engine/build.py ep01 EP001 smoke --smoke   # 6-line pipeline check

Videos are built by `engine/`, tracked in `studio.db`, and published through vidIQ after the owner approves each batch.
