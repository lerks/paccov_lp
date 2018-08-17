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


def animate(name, commands):
    tree, doc = load_template("/home/luca/slides/skeleton_notches.svg",
                              "/home/luca/slides/style.css")
    out_dir = "/home/luca/slides/videos/dynamic_%s" % name
    os.makedirs(out_dir)
    active = np.array(4 * [False])
    m = Model(A, np.array(4 * [0.0]), F, RHO, THETA)
    stage_idx = 0
    for cmd in commands:
        stage_idx += 1
        os.makedirs(os.path.join(out_dir, "stage_%d" % stage_idx))
        if cmd[0] == "add":
            active[cmd[1] - 1] = True
            prev_val = 0.0
            val = ALPHA
        elif cmd[0] == "remove":
            prev_val = m.x[cmd[1] - 1]
            val = 0
        elif cmd[0] == "raise":
            prev_val = m.x[cmd[1] - 1]
            val = prev_val * BETA
        elif cmd[0] == "lower":
            prev_val = m.x[cmd[1] - 1]
            val = prev_val / BETA
        else:
            raise ValueError("bad command: %s", cmd[0])
        for frame_idx in range(51):
            frac = evaluate_bezier(frame_idx / 50)
            frame_val = frac * val + (1 - frac) * prev_val
            m.x[cmd[1] - 1] = frame_val
            render_plots_over_time(doc, active, m, MAX_VAL, STEPS)
            render_to(tree, os.path.join(out_dir,
                                         "stage_%d" % stage_idx,
                                         "frame_%04d.png" % frame_idx))
        if cmd[0] == "remove":
            active[cmd[1] - 1] = False


animate(
    "long",
    [("add", 2),
     ("raise", 2),
     ("raise", 2),
     ("raise", 2),
     ("raise", 2),
     ("add", 3),
     ("raise", 3),
     ("raise", 3),
     ("raise", 3),
     ("lower", 2),
     ("add", 1),
     ("raise", 1),
     ("raise", 1),
     ("lower", 2),
     ("lower", 3),
     ("add", 4),
     ("raise", 4),
     ("lower", 3),
     ("raise", 4),
     ("lower", 2),
     ("remove", 2),
     ("raise", 3),
     ("raise", 1),
     ("raise", 4),
     ("remove", 3),
     ("raise", 4),
     ("raise", 1)])
