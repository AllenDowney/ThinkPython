# Plan: Colab links on every chapter

**Created:** 2026-09-29
**Board:** Task 11 in `PROJECT_BOARD.md`
**Status:** Planned, not started

## Goal

A reader on <https://allendowney.github.io/ThinkPython> should be able to open the
chapter they are reading as a runnable notebook on Colab, from every chapter.

## Current state

| | Colab link in `soln/` | Appears on the site |
|---|---|---|
| `chap00` | yes — prose in *Getting started* | yes |
| `chap01` | yes — "Welcome" cell | **no** |
| `chap02`–`chap19` | **none** | no |

Two separate problems, and the second is the larger one.

**`chap01`'s link is hidden.** Cell 1 is a `# Welcome` markdown cell containing both a
link to the Jupyter intro and a "click here to run this notebook on Colab" link
pointing at `chapters/chap01.ipynb` — the right target. The cell is tagged
`remove-cell`, which tells Jupyter Book to drop it from the rendered HTML, so the link
never reaches the website. The same applies to cell 37, which has a second Colab link
in the `%%expect` note.

The tag looks deliberate rather than accidental: the cell is written in notebook voice
("This is the Jupyter notebook for Chapter 1… if you are not already running this
notebook on Colab"), which reads wrong on a web page. Simply removing the tag would
expose prose that does not belong there.

**Chapters 2–19 have no link at all**, in `soln/`, `chapters/`, or `jb/`. There is
nothing to un-hide for 18 of the 20 chapters.

## Decision: per-chapter cell (Option B)

Add an explicit, untagged markdown cell near the top of each chapter.

**Considered and rejected: Jupyter Book's `launch_buttons`.** Setting
`launch_buttons.colab_url` in `jb/_config.yml` adds a rocket-ship button to the header
of every notebook page automatically, with no per-chapter edits. Reading
`sphinx_book_theme/header_buttons/launch.py` confirms it would work here: the URL is
built as `{colab_url}/github/{org}/{repo}/blob/{branch}/{path_rel_repo}`, and
`path_rel_repo` comes from the `path_to_docs` theme option, which Jupyter Book maps
from `repository.path_to_book`. Setting `path_to_book: chapters` would therefore
produce exactly `…/blob/v3/chapters/chapNN.ipynb`. Markdown pages (`index.md`,
`blank.md`) would be skipped, because the button is gated on `_is_notebook`, which
tests for `kernelspec` metadata.

It was rejected in favour of an explicit cell, which gives full control over wording
and placement and puts the link in the flow of the page rather than in theme chrome.
Recorded here because it remains the cheaper option if the per-chapter cells become a
maintenance burden.

### Shape of the new cell

- Untagged, so it appears in the HTML **and** in the downloadable notebooks.
- Placed immediately after the "You can order" header, as the second cell.
- Targets `chapters/chapNN.ipynb` — the student notebook, not the solution.
- Wording must work in both contexts. The current chap01 text does not: on the website
  "if you are not already running this notebook on Colab" is addressed to nobody.

### Per-chapter handling

- `chap02`–`chap19`: add the new cell.
- `chap01`: reconcile with the existing `Welcome` cell. Decide whether the Jupyter
  intro link survives, and whether the `remove-cell` tag comes off or the cell is
  replaced.
- `chap00`: already discusses Colab in *Getting started*. Check the new cell does not
  contradict or duplicate it.
- Leave cell 37 of `chap01` alone; it is a note about `%%expect`, not a launch link.

## Subtask: revise the "You can order" header

Every chapter opens with the same untagged cell, which is also stored as
`soln/header.ipynb`:

> You can order print and ebook versions of *Think Python 3e* from
> [Bookshop.org](…) and [Amazon](…).

Since the Colab cell lands directly beneath it and both are edited in the same pass,
revise it at the same time. For reference, *Think Stats* uses a more developed version:

> The third edition of *Think Stats* is available now from [Bookshop.org](…) and
> [Amazon](…) (those are affiliate links). If you are enjoying the free, online
> version, consider [buying me a coffee](https://buymeacoffee.com/allendowney).

Open questions: whether to disclose the affiliate links, whether to add the coffee
link, and whether the wording should differ between the website and the notebooks.

`soln/jntools.py` provides `add-header` and `add-footer` commands that prepend the
cells of a template notebook to a list of notebooks. Worth checking before hand-editing
20 files — though note it prepends, so it cannot replace an existing header in place,
and `header.ipynb` is currently untracked.

## Workflow

Per chapter, using the established round-trip:

```bash
cd ThinkPythonSolutions/soln
jupytext --to md chapNN.ipynb          # re-export first, so the md is fresh
#  ... edit chapNN.md ...
jupytext --update --to ipynb chapNN.md # --update preserves stored outputs
```

Keep the `.md` afterward; it is gitignored and serves as the recovery copy. Close any
Jupyter tab on a chapter before editing it.

Adding a markdown cell changes no code, so **no chapter needs re-executing** for this
task. If the header revision is the only other change, the stored outputs stay valid.

## Then: a complete build

See "Reviewing the build process" below before running anything.

---

# Reviewing the build process

There are **four** build targets, each with its own `build.sh`:

| Target | What it does | Ends with |
|---|---|---|
| `chapters/` | student notebooks + `ThinkPythonNotebooks.zip` | `git push` |
| `blank/` | code-free notebooks | `git push` |
| `jb/` | Jupyter Book HTML | `ghp-import -n -p -f` → **publishes the site** |
| top level | copies support files, renders the SVG figures | `git push` |

`ThinkPythonSolutions/update.py` claims to automate this. It should not be trusted as
written — it has two gaps that match problems actually observed in the repo:

1. **It never builds `blank/`.** It runs `chapters/`, `jb/`, and the top level only.
   This is almost certainly why `blank/` had drifted: rebuilding it on 2026-09-19
   changed 14 files, far more than the three edited chapters.

2. **It never pushes `soln/`.** Step 1 commits the solution notebooks and stops. The
   later `build.sh` runs push *ThinkPython*, so the solutions commit can sit local
   indefinitely — and two unpushed "Update solution notebooks" commits were sitting
   there on 2026-09-19.

Further problems, in rough order of severity:

3. **Failures do not stop it, and are reported as success.** `run_command` prints
   "Warning: Command exited with code N" and continues; `main` ends with
   "✓ Update process completed!" regardless. A failed `jb build` looks like a clean run.

4. **It publishes the website with no confirmation.** Step 3 runs `jb/build.sh`, which
   ends in `ghp-import -n -p -f`. Running `python update.py` pushes to GitHub Pages as
   a side effect, which is not obvious from the name or the docstring.

5. **Nothing re-executes the notebooks and nothing runs the tests.** Stored outputs are
   published exactly as they sit on disk. This is the chapter 18 failure mode: source
   corrected, output stale, published anyway.

6. **`capture_output=True` hides progress.** A multi-minute `jb build` prints nothing
   until it finishes.

7. **Step 1 commits only `soln/chap*.ipynb`.** Changes to `thinkpython.py`,
   `diagram.py` or `structshape.py` in `soln/` are silently left out.

## Recommended sequence for this task

Run the steps by hand rather than via `update.py`, or fix `update.py` first.

```text
1. edit soln/chapNN.md  ->  jupytext --update --to ipynb
2. cd ThinkPythonSolutions && make tests          # 20 chapters, ~2.5 min
3. commit and PUSH ThinkPythonSolutions
4. cd chapters && bash build.sh                   # commits + pushes ThinkPython
5. cd blank    && bash build.sh                   # the step update.py forgets
6. cd jb       && bash build.sh                   # PUBLISHES the site
7. spot-check a built page for the new Colab link before accepting the publish
```

Step 2 is cheap insurance now that all 20 chapters are under test. Step 7 matters
because the whole point of this task is a link that only appears in the rendered HTML.
