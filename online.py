import math
import os

import numpy as np

from model import Model
from svg import load_template, render_plots_over_range, render_to

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


def animate(order):
    tree, doc = load_template("/home/luca/slides/skeleton.svg",
                              "/home/luca/slides/style.css")
    out_dir = ("/home/luca/slides/videos/online_%s"
               % "_".join(str(e) for e in order))
    os.makedirs(out_dir)
    active = np.array(4 * [False])
    m = Model(A, np.array(4 * [0.0]), F, RHO, THETA)
    for stage_idx, e in enumerate(order, start=1):
        e -= 1
        active[e] = True
        os.makedirs(os.path.join(out_dir, "stage_%d" % stage_idx))
        for i in range(201):
            m.x[e] = i * math.log(2, 3) / 200
            render_plots_over_range(doc, active, m, MAX_VAL, STEPS)
            render_to(tree, os.path.join(out_dir,
                                         "stage_%d" % stage_idx,
                                         "frame_%04d.png" % i))
            if m.dual_cst(e) >= 1:
                break


animate([1, 2, 3, 4])
