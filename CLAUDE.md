# Working on Think Python

Two repositories, one book.

- **`ThinkPython`** (this one) — published artifacts: the student notebooks in
  `chapters/`, the code-free `blank/`, the Jupyter Book source in `jb/`,
  `ThinkPythonNotebooks.zip`, and the support files (`thinkpython.py`,
  `diagram.py`, `structshape.py`, `words.txt`, `photos.zip`) that the notebooks
  download at run time.
- **`ThinkPythonSolutions`** (nested at `./ThinkPythonSolutions`, a separate git
  repo) — **`soln/*.ipynb` is the canonical source of the book.** Prose, code
  and stored outputs all live there.

Edit `soln/`. Everything else is generated.

## The four build targets

| Target | Built by | What its prep step does |
|---|---|---|
| `chapters/` + zip | `chapters/build.sh` | solutions → `# Solution goes here`; **clears all tags and all outputs** |
| `blank/` | `blank/build.sh` | clears every code cell except those tagged `keep`; clears all tags and outputs |
| `jb/` → GitHub Pages | `jb/build.sh` | blanks solutions, strips `%%expect`, adds MyST anchors; **leaves tags and outputs alone** |
| top level | `build.sh` | copies support files from `soln/`, renders the SVG figures |

To build and publish everything, run `python update.py` in `ThinkPythonSolutions`.
It tests, commits and pushes `soln/`, builds all four targets, and asks before
publishing the website. Do not run the four scripts by hand unless you have a
reason — it is easy to forget `blank/`.

## Cell tags

The book leans on tags heavily, and each target reads them differently.

| tag | `chapters/` | `blank/` | `jb/` (web) | `latex/` (PDF) |
|---|---|---|---|---|
| `remove-cell` | — | — | cell dropped at render | source + outputs removed |
| `remove-output` | — | — | output hidden at render | outputs cleared |
| `remove-input` | — | — | source hidden at render | source cleared |
| `remove-print` | — | — | ignored (stays on the web) | treated as `remove-cell` |
| `solution` | source blanked | source blanked | source blanked | — |
| `keep` | — | **source preserved** | — | — |
| `chapter_*` / `section_*` | — | — | prepends a `(label)=` anchor | — |
| *all tags, all outputs* | **cleared** | **cleared** | preserved | per-tag |

`remove-print` is the tag for something that belongs on the website and in the
notebooks but not in print — the Colab links use it.

## Editing a chapter

Go through jupytext. Do not edit the `.ipynb` JSON by hand.

```bash
cd ThinkPythonSolutions/soln
jupytext --to md chapNN.ipynb          # ALWAYS re-export first
#  ... edit chapNN.md ...
jupytext --update --to ipynb chapNN.md # --update preserves stored outputs
```

Keep the `.md` afterwards. It is gitignored and serves as a recovery copy.

## Hazards

Each of these has actually bitten someone.

**`--update` is not optional.** Plain `jupytext --to ipynb` discards every
stored output. The website is built with `execute_notebooks: 'off'`, so it
renders stored outputs and never runs the code — losing them silently empties
the published chapter. Think Stats shipped three chapters with no figures for
seven months this way.

**Re-export before you edit, every time.** A stale `.md` pushed back with
`--update` overwrites whatever changed in the notebook meanwhile. This clobbered
edits to `header.ipynb` on 2026-09-29.

**Close the Jupyter tab first.** A Jupyter session saving over a chapter reverts
whatever was changed on disk underneath it.

**`remove-output` hides the output, it does not delete it.** The bytes stay in
the `.ipynb`. `chap07` reached 2.2 MB — 97% of it a word list no reader ever
sees — which made it unrenderable on GitHub and froze Colab on low-memory
machines. Run `make strip_outputs` before committing; `make tests` checks for it.

**`jb/build.sh` publishes.** It ends in `ghp-import -n -p -f`, which pushes
straight to GitHub Pages with no confirmation. `update.py` gates this behind a
prompt; the raw script does not.

**Wipe `jb/_build` before building.** Stale pages have survived in there and been
published.

**Editing `soln/header.ipynb` changes nothing on its own.** It is a template; its
text has already been copied into all 20 chapters as cell 0. Propagate after
editing it.

**The two repos push separately.** A fix in `soln/` and the rebuild of
`chapters/` are two commits in two repositories.

## Tests

```bash
cd ThinkPythonSolutions && make tests     # all 20 chapters, about 2.5 minutes
```

`make tests` runs `check_outputs.py` first, which fails the build if a chapter
was committed unexecuted, or if outputs are stored for cells no target renders.
`pytest --nbmake` cannot catch either, because it executes notebooks itself and
never looks at what is stored.

Chapter 4 is a third of the runtime on its own: `jupyturtle` sleeps
`TURTLE_DELAY` (0.2s) after each visual command and chapter 4 draws a lot.

## Known rough edges

- **Windows readers cannot run chapters 8, 11 and 12.** The book teaches
  `open(filename)` with no `encoding`, so under a cp1252 locale the Gutenberg
  texts raise `UnicodeDecodeError` on byte `0x9d`. Windows is kept out of the CI
  matrix for this reason — `PYTHONUTF8=1` would turn CI green while leaving
  readers broken.
- **Project Gutenberg downloads make CI flaky.** Chapters 8, 11 and 12 fetch
  from `gutenberg.org` at run time; the scheduled build failed on this in July
  2026. Gutenberg blocks datacenter IPs.
- **Three near-identical `prep_notebooks.py`** live in `chapters/`, `blank/` and
  `jb/`, differing by a few lines. A fix to one does not reach the others.

See `PROJECT_BOARD.md` for the numbered task list and `planning/` for longer
design notes.
