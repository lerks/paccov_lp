import math
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
THETA = 1

MAX_VAL = math.log(2, 3) * 1.1
STEPS = 1000


def animate(active):
    tree, doc = load_template("/home/luca/slides/skeleton.svg",
                              "/home/luca/slides/style.css")
    out_dir = "/home/luca/slides/videos/continuous_%s" % "_".join(
        str(e + 1) for e, active in enumerate(active) if active)
    os.makedirs(out_dir)
    still_growing = 4 * [True]
    active = np.array(active)
    m = Model(A, np.array(4 * [0.0]), F, RHO, THETA)
    step = 0
    for stage_idx in range(1, len(active) + 1):
        os.makedirs(os.path.join(out_dir, "stage_%d" % stage_idx))
        for frame_idx in range(201):
            for e, growing in enumerate(still_growing):
                if growing and active[e]:
                    m.x[e] = step * math.log(2, 3) / 200
            render_plots_over_time(doc, active, m, MAX_VAL, STEPS)
            render_to(tree, os.path.join(out_dir,
                                         "stage_%d" % stage_idx,
                                         "frame_%04d.png" % frame_idx))
            step += 1
            new_still_growing = \
                list(m.dual_cst(e) < 1 for e in range(len(still_growing)))
            if new_still_growing != still_growing:
                still_growing = new_still_growing
                break
        if not any(still_growing):
            break


animate([True, True, True, True])
