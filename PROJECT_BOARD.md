# ThinkPython Project Board

Numbered tasks for tracking work. Each task has a permanent number; add new tasks at the end. Update status as work progresses.

### Current focus (2026-09-19)

- **Task 1:** Chapter 18 `Counter` example produces nonsense output ([#78](https://github.com/AllenDowney/ThinkPython/issues/78)) — **done**; published, answered, closed.
- **Task 2:** Chapter 17 `has_pair` exercise gives the wrong outline ([#76](https://github.com/AllenDowney/ThinkPython/issues/76)) — **done**; published, answered, closed.
- **Task 3:** Student notebooks ship with every output stripped ([#79](https://github.com/AllenDowney/ThinkPython/issues/79)) — **done for Chapter 3**; published, answered, closed. Book-wide audit still open.
- **Task 4:** Project Gutenberg downloads make CI fail intermittently — not started.
- **Task 5:** Five chapters are never tested; CI is on deprecated actions and one Python version — **done** (`34bc313`), except the outputs check.
- **Task 6:** Add `dataclass` coverage to Chapter 18? ([#77](https://github.com/AllenDowney/ThinkPython/issues/77)) — editorial decision needed.
- **Task 7:** Reply to the third-party interactive edition of Chapter 3 ([#74](https://github.com/AllenDowney/ThinkPython/issues/74)) — **done**; answered and closed by Allen.
- **Task 8:** Repo hygiene and release tooling — **partly done**: `.gitignore`, nbdime, and the untracked build tooling are handled; script consolidation and stale artifacts remain.
- **Task 9:** Jupyter Book 2.0 migration — **deferred** (Jan 2026 decision).
- **Task 10:** Windows readers cannot run chapters 8, 11 and 12 — not started; confirmed.

**[#77](https://github.com/AllenDowney/ThinkPython/issues/77) is the only issue still open** — the `dataclass` question in Task 6, which needs an editorial call rather than a fix.

### How this repo fits together

`ThinkPythonSolutions/soln/*.ipynb` is the canonical source: it holds the prose, the code, and the executed outputs. Everything else is generated from it by a `prep_notebooks.py` + `build.sh` pair:

| Target | Built by | What the prep step does |
|--------|----------|-------------------------|
| `chapters/` (student notebooks, and `ThinkPythonNotebooks.zip`) | `chapters/build.sh` | Replaces solution source with `# Solution goes here`, clears tags, **clears all outputs** |
| `blank/` | `blank/build.sh` | Clears the source of every code cell except those tagged `keep`, clears all outputs |
| `jb/` → GitHub Pages | `jb/build.sh` | Blanks solution source, strips `%%expect`, adds MyST labels; **keeps outputs** |

So a content fix belongs in `ThinkPythonSolutions/soln/`, and reaches readers only after the relevant `build.sh` is re-run. The published HTML and the downloadable notebooks are prepped differently, which is the direct cause of Task 3.

### Editing a chapter

Edit through jupytext rather than the notebook JSON, and keep the `.md` afterward:

```bash
cd ThinkPythonSolutions/soln
jupytext --to md chapNN.ipynb          # re-export first, so the md is fresh
#  ... edit chapNN.md ...
jupytext --update --to ipynb chapNN.md # --update preserves stored outputs
```

`--update` merges into the existing notebook; plain `--to ipynb` would discard the outputs the website renders.

The round-trip was verified once on this repo — byte-identical, with tags (`solution`, `remove-cell`, `keep`) and `%%add_method_to` magics surviving intact. Treat that as settled; there is no need to re-check it after each conversion.

The `.md` stays on disk, untracked, as a recovery copy: an open Jupyter session saving over a chapter will silently revert edits back to HEAD, and re-applying from the markdown is far cheaper than redoing the work. Two cautions: always re-export before editing, or a stale `.md` pushed back with `--update` will clobber edits made in Jupyter; and close the Jupyter tab for a chapter before editing it here.

---

## Task 1: Chapter 18 `Counter` example produces nonsense output

**Status:** Done 2026-09-19 (`5295441`) — published, [answered](https://github.com/AllenDowney/ThinkPython/issues/78#issuecomment-5743157707) and closed.

**Reported by:** [@alchemistcai in #78](https://github.com/AllenDowney/ThinkPython/issues/78), 2026-08-16

**Location:** `ThinkPythonSolutions/soln/chap18.ipynb`, cells 39–48 (In[21], In[22], In[26] in the published numbering)

**Confirmed:** The `Counter` section introduces `counter = Counter('banana')`, then rebinds `counter = Counter(t)` where `t = (1, 1, 1, 2, 2, 3)` to demonstrate that a `Counter` accepts any sequence. Several cells later, the `+` operator is demonstrated with `counter2 = Counter('bans'); counter + counter2`. Because `counter` is still the integer version, the stored output is:

```text
Counter({1: 3, 2: 2, 3: 1, 'b': 1, 'a': 1, 'n': 1, 's': 1})
```

The surrounding prose says the `+` operator "contains the keys from both and the sums of the counts" — a point the reader cannot see in a result that mixes integers with letters and sums nothing. The example clearly intends `Counter('banana') + Counter('bans')`, which would give `Counter({'a': 4, 'n': 3, 'b': 2, 's': 1})` and actually show a sum.

**Cause:** an extra cell added to test an example and never removed. It has been deleted (25 lines out of `soln/chap18.ipynb`); `counter` is now `Counter('banana')` at the point of the `+` demonstration.

### Resolved

The notebook has since been re-executed, so source and stored output now agree. Cell 47 reads:

```python
counter2 = Counter('bans')
counter + counter2
```

and now shows `Counter({'a': 4, 'n': 3, 'b': 2, 's': 1})`, the summed counts the prose describes, in place of the old `Counter({1: 3, 2: 2, 3: 1, 'b': 1, 'a': 1, 'n': 1, 's': 1})`. Verified live in the published `chap18.html`.

### Scope

- [x] Remove the stray test cell that rebound `counter`
- [x] Re-execute `soln/chap18.ipynb` so the stored output shows the summed counts
- [ ] Check the subtraction / union / intersection follow-ons in the same section for the same stale-binding problem
- [x] Rebuild `chapters/`, `blank/`, `jb/`
- [x] Reply on #78 and close

---

## Task 2: Chapter 17 `has_pair` exercise gives the wrong outline

**Status:** Done 2026-09-19 (`5295441`) — published, [answered](https://github.com/AllenDowney/ThinkPython/issues/76#issuecomment-5743159353) and closed.

**Reported by:** [@alchemistcai in #76](https://github.com/AllenDowney/ThinkPython/issues/76), 2026-06-23

**Location:** `chapters/chap17.ipynb` cells 189–196 (In.91 in the published numbering); source in `ThinkPythonSolutions/soln/chap17.ipynb`

**Confirmed:** In `soln/`, the exercise is three cells — a `check_sets` stub, the `check_sets` body (tagged as a solution), and `has_pair` (tagged as a solution) — followed by three test cells that call `pair.has_pair()`, `bad_hand.has_pair()`, `good_hand.has_pair()`.

The prep step blanks the two solution cells, so the student notebook hands the reader this scaffolding:

```python
%%add_method_to PokerHand

    def check_sets(self, *need_list):
        return True
```

and then immediately asks them to run `pair.has_pair()`. `has_pair` is never mentioned as something to write, and the one outline they are given is for a different method. The reader's reading is correct.

**Resolution:** The outline now reads `def has_pair(self): return True`, matching the tests below it. `check_sets` is an implementation detail of the author's solution, so the reader meets it only if they read that solution — and it now carries a docstring explaining the `*need_list` convention, which is not self-evident:

```python
def check_sets(self, *need_list):
    """Checks whether this hand contains sets of cards with the same rank.

    Each argument is the size of a set we need, largest first.
    So check_sets(2) checks for a pair, check_sets(2, 2) checks for
    two pairs, and check_sets(3, 2) checks for a full house.

    need_list: sizes of the sets we need, in decreasing order
    """
```

The "largest first" requirement is load-bearing and was previously undocumented: `need_list` is zipped against the rank counts sorted descending, so `check_sets(3, 2)` recognizes a full house but `check_sets(2, 3)` does not.

### Scope

- [x] Decide the intended shape: the outline now gives `has_pair(self)`
- [x] Fix the scaffolding cell in `soln/chap17.ipynb`
- [x] Document `check_sets` so the solution is readable on its own
- [ ] Sweep the rest of Chapter 17's `%%add_method_to` exercises for the same stub/test mismatch (`has_full_house` uses the same pattern)
- [x] Rebuild and publish
- [x] Reply on #76 and close

---

## Task 3: Student notebooks ship with every output stripped

**Status:** Done for Chapter 3 on 2026-09-19 (`5295441`) — published, [answered](https://github.com/AllenDowney/ThinkPython/issues/79#issuecomment-5743154298) and closed. Book-wide audit still open.

**Reported by:** [@goekce in #79](https://github.com/AllenDowney/ThinkPython/issues/79), 2026-09-18

**Context:** A reader following Chapter 3 in the downloadable notebooks hit this prose:

> Here's an example of a rectangle with width `5` and height `4`, made up of the string `'H'`.

...with nothing after it. The rendered rectangle *is* visible at [allendowney.github.io/ThinkPython/chap03.html](https://allendowney.github.io/ThinkPython/chap03.html), so the website and the notebooks disagree about what the reader gets.

**Root cause:** The two prep scripts treat outputs differently. `jb/prep_notebooks.py` blanks the *source* of solution cells and leaves `outputs` alone, so the site still renders what the code printed. `chapters/prep_notebooks.py` does this to every cell unconditionally:

```python
# remove output
if 'outputs' in cell:
    cell['outputs'] = []
```

Result: **0 of 1370 code cells across `chapters/chap*.ipynb` have any stored output.** In the Chapter 3 case the `rectangle('H', 5, 4)` call survives (it is tagged `keep`), but the function that defines `rectangle` is `# Solution goes here` and the call has no stored result — so the reader sees a promise of an example, a blank, and a call to a function that does not exist yet.

This is a policy question, not just a bug: blank notebooks are the point, and pre-filling outputs would spoil exercises. But worked examples the prose refers to are not exercises, and today there is no way to mark one.

### The `keep` tag: what it actually does

Investigated 2026-09-19, because the tag's presence suggested a mechanism that might already solve this. It does not.

- **Exactly one script reads it:** `blank/prep_notebooks.py`, which preserves the *source* of a code cell instead of emptying it. Neither `chapters/prep_notebooks.py` nor `jb/prep_notebooks.py` mentions `keep`. So for the downloadable notebooks — the ones #79 is about — the tag has no effect whatsoever.
- **It does not preserve outputs.** Even in `blank/`, outputs are cleared unconditionally. `keep` means "keep the code," never "keep the result."
- **It was never finished.** All 18 `keep` tags in the book are in chapters 1, 2, and 3 (2, 4, and 12 respectively). Chapters 4–19 have none.
- **Two of them are on markdown cells** (`chap03` cells 77 and 79), where the `blank/` script cannot act on them at all, since it only tests `cell['cell_type'] == 'code'`.

Read together: an abandoned experiment, scoped to the first three chapters, that solves a different problem (keeping code in `blank/`) than the one in #79.

**Scale:** a scan for the "prose promises an example, solution cell follows" pattern found it only in Chapter 3 — three instances, all fixed below. The scan keyed on specific phrasings, so a wider audit is still worth doing, but this is not the book-wide problem it first looked like.

### Fix applied (Chapter 3)

Per the "keep it simple" decision: put the expected output in a preformatted block in the markdown, so the example does not depend on the solution having been run. This works in every target at once — `soln/`, `chapters/`, `blank/`, and the website — and needs no change to any prep script.

| Exercise | Block added |
|----------|-------------|
| `print_right` (cell 66) | three right-aligned lines |
| `triangle` (cell 68) | the 5-level pyramid |
| `rectangle` (cell 71) | the 4×5 rectangle — the case reported in #79 |

Verified by running `chapters/prep_notebooks.py` over the result: the reader now gets the rectangle, a `# Solution goes here` cell, and the `rectangle('H', 5, 4)` call.

**Two solution bugs found and fixed while doing this**, both of which would have contradicted the new blocks:

- `triangle` looped over `range(height+1)`, printing `string * 0` first — so "a pyramid with 5 levels" emitted a leading blank line and six lines of output. Now `range(1, height+1)`.
- `print_right`'s docstring said "column 70" while the code used `columns = 40` (the exercise asks for 40).

### Scope

- [x] Decide the rule: expected output goes in a preformatted block in the prose, not in a cell's stored output
- [x] Apply it to the three Chapter 3 exercises, including the one named in #79
- [x] Establish what `keep` does and whether it was usable here (it is not)
- [x] Re-execute `soln/chap03.ipynb` so the stored output matches the corrected `triangle`
- [ ] Wider audit for other exercises whose prose promises a result the reader cannot see
- [ ] Decide the fate of the 18 orphaned `keep` tags: finish the idea, or drop the tag and the `blank/` branch that reads it
- [x] Rebuild `chapters/`, regenerate `ThinkPythonNotebooks.zip`, publish the site
- [x] Reply on #79 and close

### Out of scope (for first pass)

- Restoring outputs for exercise solutions (that would hand readers the answers)
- Teaching `chapters/prep_notebooks.py` a `keep-output` tag — the preformatted-block approach makes it unnecessary
- Changing how the Jupyter Book build handles outputs — the site is correct today

**Known cosmetic cost:** on the website, the preformatted block and the executed output of the call cell now both appear. Tagging the call cells `remove-output` would suppress the duplicate, at the cost of changing pages that currently look right.

---

## Task 4: Project Gutenberg downloads make CI fail intermittently

**Status:** Not started

**Context:** The scheduled monthly test run for `ThinkPythonSolutions` failed on 2026-07-01 ([run 28486298964](https://github.com/AllenDowney/ThinkPythonSolutions/actions/runs/28486298964)) with:

```text
FileNotFoundError: [Errno 2] No such file or directory: 'pg345.txt'
FAILED chap08.ipynb::chap08.ipynb
```

`pg345.txt` is *Dracula*, downloaded from `gutenberg.org` at notebook-execution time. The `FileNotFoundError` is the symptom, not the cause: the `download()` helper fetched nothing (Gutenberg throttles and blocks datacenter IPs), and the next cell tried to open the file that was never written. Every run before and since has passed, so this is a live flake, not a break.

**Exposure:** `chap08`, `chap11`, and `chap12` all read Project Gutenberg texts. Runs are monthly, so a flake rate low enough to look like noise still means a red build several times a year — and a red build nobody trusts is a red build nobody reads.

### Scope

- [ ] Make `download()` fail loudly when the fetch fails, instead of leaving the next cell to raise `FileNotFoundError` on a missing file
- [ ] Decide the CI strategy: retry with backoff, mirror the three texts under a stable URL we control, or mark Gutenberg-dependent notebooks and let them fail soft in CI
- [ ] Confirm the repo's other runtime downloads (`words.txt`, `structshape.py`, `jupyturtle.py` — all on `raw.githubusercontent.com`) are not exposed the same way
- [ ] Turn on a failure notification for the scheduled run

### Out of scope (for first pass)

- Removing the live downloads from the book. They are pedagogically deliberate, and Chapter 8 is *about* reading a real text file.

---

## Task 5: Five chapters are never tested; CI is on deprecated actions

**Status:** Done 2026-09-19 (`34bc313`) — green on both legs. The outputs check is the one item left open.

**Context:** `ThinkPythonSolutions/Makefile` runs the test suite as two globs:

```makefile
tests:
	# testing notebook 04 takes too long
	cd soln; pytest --nbmake chap0[12356789]*.ipynb
	# testing notebook 12 fails on windows (unicode!)
	cd soln; pytest --nbmake chap1[1345678]*.ipynb
```

That covers 01–03, 05–09, 11, 13–18. **Chapters 00, 04, 10, 12, and 19 are never executed by CI.** Two of the exclusions are documented (04 is slow, 12 had a Windows Unicode problem); 00, 10, and 19 are silently outside the globs, and the glob encoding makes it easy to miss that.

The Windows exclusion for chapter 12 is also obsolete: the matrix is `[ubuntu-latest, macos-latest]` with the comment "don't test on windows", so 12 is excluded from a platform that is not tested anyway.

**CI configuration** (`ThinkPythonSolutions/.github/workflows/tests.yml`):

- `actions/checkout@v2` and `actions/setup-python@v2` — both run on Node 20, deprecated and being force-migrated by GitHub
- One Python version, `3.10`, released October 2021; the book teaches current Python
- No `fail-fast: false`, so one leg's failure hides the others
- No pip caching; each run reinstalls the full Jupyter stack (~2.5 min)

### What the excluded chapters actually cost

Measured before changing anything, on Python 3.10:

| Chapter | Time | Result | Why it was excluded |
|---------|------|--------|---------------------|
| `chap00` | 3s | pass | nothing — outside the glob |
| `chap10` | 5s | pass | nothing — outside the glob |
| `chap19` | 2s | pass | nothing — outside the glob |
| `chap12` | 4s | pass | "fails on windows (unicode!)" — real, but Windows is not in the matrix |
| `chap04` | 58s | pass | "takes too long" |

Four of the five cost under five seconds between them. Chapter 4 is genuinely the slow one, but the full 20-chapter suite still runs in **2m37s** — so the exclusions were buying almost nothing.

Chapter 4 is slow because `jupyturtle` sleeps `TURTLE_DELAY` (0.2s) after every visual command, and chapter 4 draws a lot. Eleven of its `make_turtle()` calls use the default delay; four already pass `delay=0`. Dropping the delay everywhere would cut the suite by a third, but it would also remove the animation that makes the turtle chapter work as teaching, so it was left alone.

**Resolution:** a plain `chap*.ipynb` glob, so a new chapter cannot be missed, plus `--durations=5` to keep slow chapters visible. CI moved to `checkout`/`setup-python` v7, Python 3.12, `fail-fast: false` and pip caching. Both legs pass.

### Scope

- [x] Replace the globs — used `chap*.ipynb`, which is stronger than a list: nothing can be omitted
- [x] Get 00, 10, and 19 into the suite
- [x] Re-test chapter 12 and drop the stale Windows comment
- [x] Decide on chapter 04 — measured at 58s and included
- [x] Bump `checkout` and `setup-python` to v7; Python 3.12; `fail-fast: false`; pip caching
- [ ] Add an outputs check: a `soln/` notebook committed with `execution_count: null` throughout should fail the build (`--nbmake` executes notebooks, so stored outputs are invisible to it — this is the check that catches a chapter committed unexecuted)

---

## Task 6: Add `dataclass` coverage to Chapter 18?

**Status:** Editorial decision needed

**Requested by:** [@alchemistcai in #77](https://github.com/AllenDowney/ThinkPython/issues/77), 2026-06-30

**Context:** Chapter 18 covers `namedtuple` and `Counter` from the standard library. The request is to add `dataclasses` alongside `namedtuple`: in the standard library since 3.7, mutable, supports methods, and less boilerplate than a hand-written class — a natural complement to the immutable `namedtuple`.

The counter-argument is scope. Chapter 18 is the "Python extras" chapter near the end of a book that has already taught classes the long way, and a third edition is not a place to add topics without a reason. The decision is whether `dataclass` is now common enough in real code that a reader who finishes this book and does not recognize it has a gap.

### Scope

- [ ] Decide: full section, a short aside next to `namedtuple`, an exercise, or decline
- [ ] If adding: draft, execute, and keep the chapter's length in check
- [ ] Reply on #77 either way

---

## Task 7: Reply to the third-party interactive edition of Chapter 3

**Status:** Done 2026-09-19 — Allen replied and closed the issue.

**Context:** [@ling-k in #74](https://github.com/AllenDowney/ThinkPython/issues/74) (2026-04-22) built an interactive edition of Chapter 3 — live Python execution in the exercise blocks plus a chapter-grounded AI tutor — at `xlearnhub.com`, under CC BY-NC 3.0, with more chapters in progress. They made no ask and offered to take it down or change anything.

Open since April with no reply. Two things worth separating: whether the attribution and license terms are met (the book is CC BY-NC, so a non-commercial derivative with attribution is within the license), and whether this is something to link from the book's home page or leave alone.

### Scope

- [x] Look at the demo and check the attribution and license notice
- [x] Decide whether to acknowledge, link, or simply thank and close
- [x] Reply on #74

---

## Task 8: Repo hygiene and release tooling

**Status:** Not started

**Context:** `git status` on `v3` reports 58 untracked paths, which makes it useless as a signal — a real change is invisible in the noise. The causes are separable:

**Generated files that are neither tracked nor ignored.** `jb/*.ipynb` (all 20 chapters), `chapters/thinkpython.py`, `chapters/diagram.py`, `chapters/structshape.py`, `chapters/words.txt`, `chapters/photos.zip`, `blank/*` support files — all copied in by a `build.sh` on every build. `.gitignore` is the stock Python template and mentions none of them. They should be ignored (if generated) or tracked (if not); right now they are neither.

**Build scripts that are half-tracked.** `chapters/build.sh`, `jb/build.sh`, and `jb/prep_notebooks.py` are in version control. The top-level `build.sh`, `blank/build.sh`, `blank/prep_notebooks.py`, and `chapters/prep_notebooks.py` are not — so the script that causes Task 3 has no history and exists only on this machine.

**Four near-identical copies of the same script.** `prep_notebooks.py` exists in `chapters/`, `blank/`, and `jb/`, differing in a handful of lines (see the table at the top). A fifth file, `chapters/prep_notebook.py`, is singular and separate. A fix to one does not reach the others.

**Stale artifacts at top level.** `ThinkPython3Notebooks.zip` (517 KB, March 2024) predates the rename to `ThinkPythonNotebooks.zip`; `ThinkPythonSolutionsNotebooks.zip` (557 KB, July 2024) is 14 months stale against a solutions repo that has moved since. Both are tracked, so both are served to anyone who clones. `Turtle.py` (20 KB, January 2024) is tracked and referenced by nothing — Chapter 16 uses `jupyturtle`. `du` is 17 KB of captured `du` output, untracked, sitting at the top level.

**The same problem in `ThinkPythonSolutions`.** `git status` there reports ~50 untracked paths in `soln/` alone: `__pycache__/`, `.ipynb_checkpoints/`, downloaded corpora (`pg345.txt`, `pg1184.txt`, `pg43.txt` and seven derived files), scratch notebooks (`testing_zone.ipynb`, `color_explorations.ipynb`), an `old/` directory, and generated `.dbm` files. The downloads in particular are produced by running the notebooks, so they reappear after every test run.

**`nbdime` is configured but not installed.** `git diff` on any notebook in `ThinkPythonSolutions` fails outright:

```text
ModuleNotFoundError: No module named 'nbdime'
fatal: external diff died, stopping at soln/chap17.ipynb
```

The diff driver is set in git config, so every notebook diff needs `--no-ext-diff` to work at all. Either install `nbdime` or drop the driver.

**No `CLAUDE.md`.** The traps in this repo are not guessable: `soln/` is canonical and everything else is generated; `jb/build.sh` ends in `ghp-import -n -p -f` and publishes to GitHub Pages with no confirmation; the three prep scripts diverge in ways that matter; `ThinkPythonSolutions` is a separate git repo nested inside this one, so a content fix and its rebuild are two commits in two repos.

### Scope

- [ ] Write a real `.gitignore` in both repos: generated notebooks, copied support files, downloaded corpora, `__pycache__/`, `.ipynb_checkpoints/`
- [ ] Install `nbdime` or remove the git diff driver that depends on it
- [ ] Track every build and prep script, or move them somewhere that is tracked
- [ ] Consolidate the three `prep_notebooks.py` variants into one parameterized script (this is also the cleanest fix for Task 3)
- [ ] Delete `ThinkPython3Notebooks.zip`, `ThinkPythonSolutionsNotebooks.zip`, `Turtle.py`, and `du`; decide whether the solutions zip should be regenerated or dropped
- [ ] Commit `planning/` or move it out of the working tree
- [ ] Write `CLAUDE.md` covering the hazards above
- [ ] Document the release ritual end to end: fix in `soln/` → rebuild `chapters/`, `blank/`, `jb/` → commit in both repos → publish

### Out of scope (for first pass)

- Merging `ThinkPythonSolutions` into this repo or converting it to a submodule
- Changing the GitHub Pages deployment mechanism

---

## Task 9: Jupyter Book 2.0 migration

**Status:** ⏸️ Deferred indefinitely (decision recorded 2026-01-12)

**Context:** A full migration plan from Jupyter Book 1.x to 2.0 was researched and written in January 2026, then shelved. The reasoning, from `planning/jupyter_2_plan.md`:

> Too many critical unknowns (notebook execution settings, CC license footer, MyST extensions configuration) combined with a perfectly functioning JB 1.x setup. No compelling reason to risk breaking a working system.

The current `jb/` build uses `_config.yml` + `_toc.yml` with thirteen MyST extensions, a custom MathJax configuration, a Creative Commons license footer, and `execute_notebooks: 'off'` — none of which have a verified 2.0 equivalent. The reference implementations that prompted the idea (`BayesFertility/jb`, `EqualityWEF/HALE/jb`) are much smaller books.

**Preserved planning material** (in `planning/`, currently untracked — see Task 8):

| File | Contents |
|------|----------|
| `jupyter_2_plan.md` | Full phased plan, decision record, risk summary |
| `config_mapping.md` | `_config.yml` + `_toc.yml` → `myst.yml`, mapped field by field |
| `issues_analysis.md` | Risk-ranked analysis of what breaks under 2.0 |
| `file_organization_plan.md` | Proposed `jb2/` layout for a side-by-side migration |

**Revisit if:** Jupyter Book 1.x stops receiving fixes, a dependency conflict forces the issue, or a 2.0-only feature becomes worth the risk.

### Scope (only if reopened)

- [ ] Re-validate `config_mapping.md` against the then-current 2.0 release
- [ ] Build `jb2/` side by side, leaving `jb/` untouched until the output matches
- [ ] Confirm the unknowns: execution settings, CC footer, MyST extension parity, MathJax config

---

## Task 10: Windows readers cannot run the Project Gutenberg chapters

**Status:** Not started; confirmed 2026-09-19

**Context:** Surfaced while doing Task 5, from the old Makefile comment "testing notebook 12 fails on windows (unicode!)". The comment was right about the symptom and wrong about the scope.

The book teaches file reading in its simplest form — `open(filename)`, with no `encoding` argument. **No `open()` call anywhere in the book passes one.** In text mode Python then uses the locale's preferred encoding, which on a default Windows install is cp1252. The Project Gutenberg texts are UTF-8, and they contain bytes that cp1252 does not define:

```text
pg43.txt     UnicodeDecodeError -- byte 0x9d at offset 2295
pg345.txt    UnicodeDecodeError -- byte 0x9d at offset 1883
pg1184.txt   UnicodeDecodeError -- byte 0x9d at offset 6927
```

`words.txt` is unaffected — it is ASCII, so it decodes without error under either.

**Who this hits:** chapters 8, 11 and 12 — not just 12, as the comment implied. This is not a CI artifact. A reader on Windows who downloads the notebooks and runs chapter 8 gets a traceback on the first `open()`, in the chapter that introduces reading files.

**Why it is still open:** the fix is an editorial call, not a technical one.

- Adding `encoding='utf-8'` to the affected `open()` calls fixes readers and CI together, but introduces a parameter the chapter has not taught yet, in the exact example meant to show how simple reading a file is.
- Setting `PYTHONUTF8=1` in CI would turn the Windows leg green while leaving readers exactly as broken. That is worse than not testing Windows, which is why the matrix still excludes it.
- The problem self-resolves on Python 3.15, where UTF-8 mode becomes the default (PEP 686). That is a real argument for waiting, and no argument at all for readers on today's Python.

### Scope

- [ ] Decide whether the book teaches `encoding='utf-8'` when reading downloaded text, and if so where it is introduced
- [ ] Apply it to chapters 8, 11 and 12
- [ ] Add `windows-latest` back to the CI matrix once the chapters pass without `PYTHONUTF8`
- [ ] Check whether any reader has already reported this
