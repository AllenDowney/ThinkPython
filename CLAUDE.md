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

**Prepping is destructive, not idempotent.** `prep_notebooks.py` at the top
level serves both `chapters/` and `blank/` (`python ../prep_notebooks.py
chapters|blank`); `jb/prep_notebooks.py` stays separate because it does a
different job. The prep clears every tag, so a second run no longer sees `keep`
and empties the cells the reader needs — 2, 4 and 10 cells of code in chapters
1 to 3. `build.sh` always copies fresh from `soln/` first, so the release path
is safe; the trap is running the script by hand. It now refuses when every
notebook in the directory is untagged. Note `chap00` and `chap19` carry no tags
even in `soln/`, so the check requires *all* of them to be bare.

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

- **The Gutenberg chapters read with an explicit encoding, on purpose.**
  Chapters 8, 11 and 12 pass `encoding='utf-8'` to every `open()` of a
  Gutenberg-derived file, including the writers. Without it, Windows uses its
  cp1252 locale default and raises `UnicodeDecodeError` on byte `0x9d`. Each
  chapter carries a short note tagged `remove-print` saying the argument is not
  in the printed book. Do not "simplify" these back, and do not paper over a red
  Windows CI leg with `PYTHONUTF8=1` — readers do not have that set either.
  `words.txt` is deliberately left plain: it is ASCII, and it is what the simple
  teaching examples use.
- **The Project Gutenberg texts are served from this repo, not gutenberg.org.**
  `pg345.txt`, `pg1184.txt` and `pg43.txt` are tracked at the top level and the
  chapters download them from `github.com/AllenDowney/ThinkPython/raw/v3/`.
  Gutenberg blocks datacenter IPs, which broke CI in July 2026, and all three
  files had drifted from the copies the stored outputs were computed against.
  Do not point these back at gutenberg.org.
- **The first edition is on the `v1` branch** (renamed from `master`,
  2026-10-30). `v3` is this book and the default branch.

See `PROJECT_BOARD.md` for the numbered task list and `planning/` for longer
design notes.
