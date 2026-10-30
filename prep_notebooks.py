#!/usr/bin/env python3
"""Strip solutions from the notebooks copied into chapters/ or blank/.

Run from inside the target directory, after its build.sh has copied the
chapters in from ThinkPythonSolutions/soln:

    cd chapters && python ../prep_notebooks.py chapters
    cd blank    && python ../prep_notebooks.py blank

Both modes clear every tag and every stored output. They differ in what
happens to the code:

    chapters   solution cells become `# Solution goes here`; other code
               is left for the reader to run
    blank      every code cell is emptied, except cells tagged `keep`,
               whose code the reader needs in order to continue

This replaces the near-identical copies that used to live in chapters/ and
blank/. They drifted, which is the class of bug behind ThinkPython#79.

jb/prep_notebooks.py is deliberately separate: it does a different job
(keeps tags and outputs, adds MyST anchors, writes the page descriptions
from descriptions.yml) and shares no logic with these two.
"""

import argparse
from glob import glob

import nbformat as nbf

SOLUTION_PREFIX = "# Solution"
PLACEHOLDER = "# Solution goes here"


def prep_cell(cell, mode):
    # Tags are build-time instructions, not something readers need.
    tags = cell["metadata"].get("tags", [])
    if "tags" in cell["metadata"]:
        cell["metadata"]["tags"] = []

    # Readers run the notebooks themselves.
    if "outputs" in cell:
        cell["outputs"] = []

    if mode == "chapters":
        if cell["source"].startswith(SOLUTION_PREFIX) or "solution" in tags:
            cell["source"] = PLACEHOLDER
    else:
        if cell["cell_type"] == "code" and "keep" not in tags:
            cell["source"] = ""


def already_prepped(ntbk):
    """True if this notebook has been through a prep already.

    Every chapter in soln/ carries tags. Prepping clears them, so a notebook
    with no tags at all has already been processed. Running again would be
    destructive rather than idempotent: with the `keep` tags gone, blank mode
    empties the very cells it was supposed to preserve -- in chapters 1 to 3
    that is 2, 4 and 10 cells of code the reader needs to continue.
    """
    return not any(cell["metadata"].get("tags") for cell in ntbk.cells)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=["chapters", "blank"])
    parser.add_argument("--force", action="store_true",
                        help="prep even if the notebooks look already prepped")
    args = parser.parse_args()

    paths = sorted(glob("chap*.ipynb"))
    if not paths:
        raise SystemExit("no chap*.ipynb here -- run this from chapters/ or blank/, "
                         "after build.sh has copied the notebooks in")

    notebooks = [(p, nbf.read(p, nbf.NO_CONVERT)) for p in paths]
    # Only refuse when EVERY notebook is untagged. Some chapters legitimately
    # carry no tags in soln/ -- chap00 and chap19 are prose with one empty code
    # cell -- so "any untagged" would block a perfectly fresh copy.
    if all(already_prepped(nb) for _, nb in notebooks) and not args.force:
        raise SystemExit(
            f"All {len(paths)} notebooks here have no tags, so they have already "
            "been prepped.\nRunning again would empty the `keep` cells. Copy fresh "
            "notebooks from ThinkPythonSolutions/soln first\n(build.sh does this), "
            "or pass --force if you are certain."
        )

    for path, ntbk in notebooks:
        print(f"Removing solutions from {path}")
        for cell in ntbk.cells:
            prep_cell(cell, args.mode)
        nbf.write(ntbk, path)


if __name__ == "__main__":
    main()
