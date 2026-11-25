"""Re-render only the motion segments whose drawings changed (timing unchanged), then run the ffmpeg line from build.py.
render2.py 2 splits the video into six equal segments, seg/s000.mp4 to s005.mp4; segment k covers total/6*k to total/6*(k+1) seconds.

    cd work/EP006 && THSQ_EP=ep06 PYTHONPATH=../../engine python3 ../../engine/tools/reseg.py 0 1"""
import sys, math
from multiprocessing import Pool
import render2 as R
n = 6; step = math.ceil(R.N/n); jobs = [(k, k*step, min(R.N, (k+1)*step)) for k in map(int, sys.argv[1:])]
if __name__ == "__main__":
    with Pool(2) as pool:
        for k in pool.imap_unordered(R.seg, jobs): print("seg", k, flush=True)
