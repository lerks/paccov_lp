import os
import subprocess
import tempfile
import xml.etree.ElementTree
import numpy as np

from model import Model, plot_dual_cst_over_range, plot_dual_cst_over_time


SVG_NAMESPACE = "http://www.w3.org/2000/svg"
NS = {"": "http://www.w3.org/2000/svg"}

xml.etree.ElementTree.register_namespace("", SVG_NAMESPACE)


def load_template(template_path, stylesheet_path):
    tree = xml.etree.ElementTree.parse(template_path)
    doc = tree.getroot()
    style = xml.etree.ElementTree.Element("{%s}style" % SVG_NAMESPACE)
    with open(stylesheet_path, "rt") as f:
        style.text = f.read()
    doc.insert(0, style)
    return tree, doc


def render_plots_over_range(
        doc: xml.etree.ElementTree.Element,
        edges_present: np.ndarray,
        model: Model,
        max_val: float,
        steps: int):
    for e in range(4):
        edge = doc.find(".//*[@id='edge_%d']" % (e + 1), NS)
        group = doc.find(".//*[@id='edge_%d_group']" % (e + 1), NS)
        if not edges_present[e]:
            assert model.primal_var(e) == 0
            group.set("style", "opacity: 0")
            edge.set("style", "opacity: 0")
        else:
            group.set("style", "opacity: 1")
            group.find(".//*[@class='gauge']", NS) \
                .set("d", "M 0,0 H %g" % (model.primal_var(e) / max_val))
            group.find(".//*[@class='cst_start']", NS) \
                .set("cy", "%f" % (135 - model.dual_cst_at(e, 0) * 90))
            group.find(".//*[@class='cst_plot']", NS) \
                .set("d", plot_dual_cst_over_range(
                    model, e, model.primal_var(e), max_val, steps))
            edge.set("style", "opacity: 1")
            edge.set("style", "fill-opacity: %f" % (model.primal_var(e)))


def render_plots_over_time(
        doc: xml.etree.ElementTree.Element,
        edges_present: np.ndarray,
        model: Model,
        max_val: float,
        steps: int):
    for e in range(4):
        edge = doc.find(".//*[@id='edge_%d']" % (e + 1), NS)
        group = doc.find(".//*[@id='edge_%d_group']" % (e + 1), NS)
        if not edges_present[e]:
            assert model.primal_var(e) == 0
            group.set("style", "opacity: 0")
            edge.set("style", "opacity: 0")
        else:
            group.set("style", "opacity: 1")
            group.find(".//*[@class='gauge']", NS) \
                .set("d", "M 0,0 H %g" % (model.primal_var(e) / max_val))
            group.find(".//*[@class='cst_plot']", NS) \
                .set("d", plot_dual_cst_over_time(model, e, model.primal_var(e),
                                                  max_val, steps))
            edge.set("style", "opacity: 1")
            edge.set("style", "fill-opacity: %f" % model.primal_var(e))


def render_to_using_imagemagick(tree, out_path):
    out_end, in_end = os.pipe()
    os.set_inheritable(out_end, True)
    process = subprocess.Popen(
        ["convert", "-",
         "-crop", "600x380+20+80",
         out_path],
        stdin=out_end)
    os.close(out_end)
    tree.write(open(in_end, "wb", closefd=False))
    os.close(in_end)
    process.wait()


def render_to_using_inkscape(tree, out_path):
    with tempfile.NamedTemporaryFile(suffix=".svg") as f:
        tree.write(f)
        f.flush()
        subprocess.call(
            ["inkscape", "-z", f.name,
             "-e", out_path,
             "-a", "20:20:620:400",
             "-b", "white",
             "-d", "192",
             # "-w", str(2 * 600),
             # "-h", str(2 * 380),
             ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL)


render_to = render_to_using_inkscape
