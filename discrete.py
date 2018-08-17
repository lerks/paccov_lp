import os

import numpy as np

from model import Model
from svg import load_template, render_plots_over_time, render_to

A = np.array([[1, 0, 0, 0],
              [1, 1, 1, 0],
              [0, 1, 0, 1],
              [0, 0, 1, 1]])
F = 2
D = 3
RHO = 1
BETA = 4 / 3
EPSILON = 1 / 3
THETA = 2.72161
ALPHA = 0.124018
L = 4

MAX_VAL = ALPHA * (BETA ** L) * 1.1
STEPS = 1000


X_1 = 0.42
Y_1 = 0
X_2 = 0.58
Y_2 = 1


def evaluate_bezier(x):
    ts = np.roots([3 * X_1 - 3 * X_2 + 1,
                   -6 * X_1 + 3 * X_2,
                   3 * X_1,
                   -x])
    t = None
    for i in range(3):
        if ts[i].imag == 0:
            t = ts[i].real
            break
    return (3 * (1 - t) ** 2 * t * Y_1
            + 3 * (1 - t) * t ** 2 * Y_2
            + t ** 3)


def animate(active):
    tree, doc = load_template("/home/luca/slides/skeleton_notches.svg",
                              "/home/luca/slides/style.css")
    out_dir = "/home/luca/slides/videos/discrete_%s" % "_".join(
        str(e + 1) for e, active in enumerate(active) if active)
    os.makedirs(out_dir)
    still_growing = 4 * [True]
    active = np.array(active)
    m = Model(A, np.array(4 * [0.0]), F, RHO, THETA)
    prev_val = 0
    for stage_idx in range(0, L + 1):
        os.makedirs(os.path.join(out_dir, "stage_%d" % stage_idx))
        val = ALPHA * BETA ** stage_idx
        for frame_idx in range(101):
            frac = evaluate_bezier(frame_idx / 100)
            frame_val = frac * val + (1 - frac) * prev_val
            for e, growing in enumerate(still_growing):
                if growing and active[e]:
                    m.x[e] = frame_val
            render_plots_over_time(doc, active, m, MAX_VAL, STEPS)
            render_to(tree, os.path.join(out_dir,
                                         "stage_%d" % stage_idx,
                                         "frame_%04d.png" % frame_idx))
        still_growing = \
            list(m.dual_cst(e) < 1 for e in range(len(still_growing)))
        if not any(still_growing):
            break
        prev_val = val


animate([True, True, True, True])
