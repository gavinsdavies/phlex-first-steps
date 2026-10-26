"""Tag notebook cells for RISE (jupyterlab-rise) slides, the way Alex Booth's ND tutorial does.

    python3 tag_slides.py notebook.ipynb [more.ipynb ...]   # edits the files in place

Rules, from the first line of each cell:
- a markdown cell that starts with "# "   -> slide     (a new slide, left to right)
- a markdown cell that starts with "## "  -> subslide  (a new slide under it, top to bottom)
- a code cell that is a catch-up or solution cell -> skip (not shown when presenting)
- the "⏭️ Catch-up" note above a catch-up cell      -> skip
- everything else                          -> fragment  (appears on the current slide)

The notebook still works as a normal notebook: the tags only change how RISE shows it.
Files are rewritten with the same JSON layout they had, so the diff is only the tags.
build_nb.py calls tag() itself, so phlex-first-steps.ipynb is tagged on every rebuild.
"""
import json
import sys

# Same presentation settings as Alex's tutorial-DUNENDSim notebooks
RISE = {
    "autolaunch": False,
    "enable_chalkboard": True,
    "height": "100%",
    "scroll": True,  # long cells and outputs scroll instead of being cut off
    "theme": "solarized",
    "transition": "slide",
    "width": "100%",
}

HIDDEN = ("# catch-up", "# solution")


def first_line(cell):
    src = cell["source"]
    if isinstance(src, list):
        src = "".join(src)
    for line in src.splitlines():
        if line.strip() and not line.startswith("%%"):  # skip cell magics such as %%bash
            return line.strip()
    return ""


def slide_type(cell):
    line = first_line(cell)
    if cell["cell_type"] == "markdown":
        if line.startswith("> ⏭️"):
            return "skip"
        if line.startswith("# "):
            return "slide"
        if line.startswith("## "):
            return "subslide"
    elif cell["cell_type"] == "code" and line.lower().startswith(HIDDEN):
        return "skip"
    return "fragment"


def tag(nb):
    """Tag every cell of a notebook (a dict or an nbformat NotebookNode) and add the RISE settings."""
    for cell in nb["cells"]:
        cell.setdefault("metadata", {})["slideshow"] = {"slide_type": slide_type(cell)}
    nb["metadata"]["rise"] = dict(RISE)
    return nb


def tag_file(path):
    raw = open(path, encoding="utf-8").read()
    nb = json.loads(raw)
    # Keep the file's own layout: nbformat writes non-ASCII as is, plain json.dump escapes it
    ascii_ = json.dumps(nb, indent=1, ensure_ascii=False) + "\n" != raw
    tag(nb)
    with open(path, "w", encoding="utf-8") as f:
        f.write(json.dumps(nb, indent=1, ensure_ascii=ascii_) + "\n")
    counts = {}
    for cell in nb["cells"]:
        t = cell["metadata"]["slideshow"]["slide_type"]
        counts[t] = counts.get(t, 0) + 1
    print(f"{path}: {counts}")


if __name__ == "__main__":
    for p in sys.argv[1:]:
        tag_file(p)
