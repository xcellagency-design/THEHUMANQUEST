"""Which episode the pipeline scripts work on. THSQ_EP=ep02 selects engine/ep02.py; THSQ_UNITS=6 keeps the first 6 lines (smoke tests)."""
import os, importlib
U = importlib.import_module(os.environ.get("THSQ_EP", "ep01")).U
if os.environ.get("THSQ_UNITS"): U = U[: int(os.environ["THSQ_UNITS"])]
