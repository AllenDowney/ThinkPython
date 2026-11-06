# Plan: Archive and mine the old Software Design materials

**Created:** 2026-11-06
**Board:** Task 18 in `PROJECT_BOARD.md` (feeds Task 17, teaching materials)
**Status:** Steps 1 to 3 done 2026-11-06: 418 questions cataloged, 314 distinct (`ThinkPythonTeaching` `9875d79`). Mining under way: Chapters 2–6, 9–11 and 14–17 done 2026-11-06

## Goal

Allen taught Software Design from *Think Python* for many years. The quizzes, exams,
homework and solutions from those offerings are scattered across Canvas, old Google
Sites and this disk. Gather them into one archive with a record of where each item
came from, then mine it for material for teachers (Task 17): more quiz questions, a
private exam bank, in-class activities and assignments.

## Sources (surveyed 2026-11-06)

| Source | Where | Terms | Files | Quiz/exam/hw-named | Formats | Already public? |
|---|---|---|---|---|---|---|
| Old course web pages | `~/AllenDowneyCom/allendowney/sd04fall`, `sd06spr`, `sd07spr`, `sd08spr` | Fall 2004, Spring 2006 to 2008 | 1,203 | 387 | HTML, PDF handouts (`handouts/quiz01.pdf`…) | **Yes**: live on allendowney.com; the AllenDowneyCom repo is private |
| Subversion checkouts | `~/svn/sd11s`, `~/svn/sd13fa` (and `~/svn.old/sd11s`, an older copy of `sd11s`) | Spring 2011, Fall 2013 | 449 | 126 | LaTeX quizzes and exams, `*_soln.txt` solutions, `code/*_code.py` | No |
| Google Sites (downloaded) | `~/Downloads/DataScience/sites.google.com/site/softwaredesign11spr`, `softwaredesign11f`, `sd13fa` | Spring 2011, Fall 2011, Fall 2013 | 292 | 32 | HTML pages, attached PDFs and `.py` (filenames carry `?attredirects=0`) | **Yes**: `sites.google.com/site/sd13fa` still loads |
| `~/SoftwareDesign` | git repo | Fall 2013 | 53 | 3 | chapter code, `swampy`, `pdb` | Unknown |
| **External drive** (the largest source) | `/media/downey/My Passport/rocky/sd04spr`, `sd04fall`, `sd06spr`, `sd07spr`, `sd08spr`, `sd11s`, `sd11f` (`sd` is a symlink to `sd08spr`) | Spring 2004 to Fall 2011 | about 11,600 | about 1,030 | LaTeX, PDF, HTML, Python, Subversion working copies | No, but **contains student records** (below) |
| Canvas (Olin) | — | — | — | — | — | **None**: what Allen remembered as Canvas is the external drive |
| `~/svn/sd11f` | — | Fall 2011 | 0 | — | empty checkout | — |

Not included: `~/ss12`, which has many quizzes and exams but is Software Systems
(Spring 2008; its LaTeX says `\course{Software Systems}`), a C course.

**Allen's classes page** ([allendowney.com/wp/classes](https://www.allendowney.com/wp/classes/))
lists Software Design for Spring 2011, Fall 2011 and Fall 2013, all on Google Sites, and
all three are already downloaded locally. Its Canvas links (canvas.olin.edu and
canvas.instructure.com) are other courses: Data Science, Data Structures and
Algorithms, Complexity Science, and Modeling and Simulation. So the Software Design
terms before 2011 exist only as the allendowney.com pages (2004 to 2008); 2005 and
2009 to 2010 are unaccounted for.

### Exporting from Google Sites

The three Software Design sites are classic Google Sites (`sites.google.com/site/…`).
Google retired classic Sites in 2021: each unconverted site was saved as a **Takeout
archive in its owner's Google Drive** and replaced with a draft in new Sites. The
classic-Sites export tools were gone by early 2025. In order of preference:

1. **The 2021 Takeout archives in Allen's Drive**, if they exist: the most faithful
   copy, with the pages as HTML and every attachment. Search Drive for "Takeout" or the
   site names. (Claude can't search Drive until the Google Drive connector is
   authorized.)
2. **Google Takeout → Google Sites**, for the converted new-format sites: HTML pages
   plus images and attachments. It only works on sites in My Drive.
3. **A crawl of the public site** (`wget --mirror`). That is what the copies in
   `~/Downloads/DataScience/sites.google.com/` are, judging by the `?attredirects=0`
   filenames. It misses unpublished pages and unlinked attachments.

For these three sites the crawl already exists; use the Takeout archive as well if it
turns up, and diff the two. Also outside scope: the Canvas quizzes for Think
Complexity, Data Science, Graphics and Probability.

### What the material will need

- **Python 2.** Everything here predates the 3rd edition: `print` statements,
  integer division, `raw_input`, `dict.has_key`, and so on. Every question needs
  checking against Python 3, by running its code.
- **Old chapter numbers.** The quizzes follow the 1st or 2nd edition, whose chapters
  differ from the 3rd's (turtles, recursion, files and the case studies all moved).
  Questions have to be mapped by topic, not by number.
- **Swampy.** Older material uses `swampy` (TurtleWorld, World, Lumpy), which the
  3rd edition replaced with `jupyturtle` and `diagram.py`.
- **Duplicates.** `svn.old/sd11s` is nearly the same as `svn/sd11s`; the downloaded
  Google Sites duplicate some of the Subversion files; questions were reused from term
  to term.
- **Solutions are patchy.** Some exams have `_soln.txt` files; many quizzes don't.

### Student records: keep them out

The original course folders, especially on the external drive, hold more than course
material: class lists (`classlist.txt`, `classl.cgi*`), grade spreadsheets
(`*grades*`, `*.xls`, `*.ods`, `exam1.scores`), address books and email lists, student
photos (`sd06spr/photos`, `sd07spr/photos`), and per-student work (`svn/<student>/`,
most of `sd11f`, which is `repos/` plus `sd11f_repos.zip`). None of it goes into the
archive, private or not. Gathering works from an **allowlist** of instructor-written
material (quizzes, exams, solutions, homework and project handouts, lecture notes,
example code) and logs what it skipped, for Allen to check.

Not included either: `rocky/sdsc` (San Diego Supercomputer Center tarballs).

## Where the archive lives

The archive holds exam and quiz answers, so it shouldn't go in this repository or
ThinkPythonSolutions, which are both public. Options:

1. **A new private repository**, e.g. `ThinkPythonTeaching`, nested here like
   ThinkPythonSolutions and gitignored by this repo. It's versioned and backed up, and
   it can later hold the private materials Task 17 produces.
2. **A local folder**, gitignored, e.g. `~/ThinkPython/teaching_archive/`. Simplest,
   but not backed up or shareable.

**Decided 2026-11-06: option 1.** Created
[`AllenDowney/ThinkPythonTeaching`](https://github.com/AllenDowney/ThinkPythonTeaching)
(private), cloned at `~/ThinkPython/ThinkPythonTeaching` and gitignored by this repo.
Its README says it must stay private and must never hold student data. It will also
hold Task 17's private exam bank and assignments.

## Gathered (2026-11-06)

`ThinkPythonTeaching/tools/gather.py` built `archive/<term>/<source>/` from the
sources above: 1,863 files, 64 MB, for 2004 (spring and fall), 2006 to 2008 (spring),
2011 (spring and fall) and 2013 (fall). By filename, that includes about 165 quiz, 75
exam, 59 warmup and 69 solution files, plus homework, labs, notes and syllabi.
`archive/SOURCES.md` records where each folder came from, and `archive/SKIPPED.tsv`
lists everything left out.

Rules that came out of looking at the data:

- **Student folders** are named `first.last` (including hyphenated surnames):
  skipped, except `allen.downey`. 7,031 files.
- **`projects/`** holds student final projects in every term that has it (2004 fall
  even has crawls of `students.olin.edu`): skipped, 3,152 files. `project/`
  (singular) is Allen's project handout and is kept. `repos/` (Fall 2011): 2,193 files.
- **Possible student data** by filename (class lists, grades, address books, email
  lists, spreadsheets): 79 files skipped.
- **The log names no students.** Skips in those categories are logged as counts per
  term only; a check confirmed no email addresses or `first.last` folders in
  `SKIPPED.tsv` or in the copied paths.
- Also skipped: 1,415 duplicates across sources, images, build files, backups and
  version-control folders. Fall 2011 on the drive was entirely student repos; that
  term's material comes from the Google Site.

## Converted and cataloged (2026-11-06)

`tools/to_text.py` mirrors `archive/` into `text/` (1,590 files): LaTeX and HTML
through `pandoc`, PDFs through `pdftotext` only when no LaTeX or HTML version exists,
`.doc` through LibreOffice. The quizzes use two custom macros that `pandoc` can't
render: `\blank{…}` (a fill-in line, which would silently vanish) and `\ls{…}`
(line spacing, which left junk), so the LaTeX is pre-processed first. 7 PDFs have no
text layer (scanned handouts and a book chapter); 6 failed LaTeX files are LaTeX-to-HTML
scratch files.

`tools/catalog_files.py` writes `catalog/files.csv`: about 170 distinct quizzes, exams
and warmups (typically 11 quizzes, 3 or 4 exams and 10 warmups per term), 247
homework files and 59 labs. Only 2 or 3 assessments per term have a solution file.
Question counts in the CSV are lower bounds.

## Question catalog (2026-11-06)

Eight subagents, one per term, cataloged every quiz, exam and warmup question
against a fixed brief (`catalog/questions/BRIEF.md`): verbatim text, type, topics,
3rd-edition chapter, Python 2 and Swampy issues, solution where one exists, and a
reusability rating. `tools/merge_catalog.py` merges them into `catalog/questions.json`,
groups repeats across terms, and writes `catalog/REPORT.md`, one entry per distinct
question by chapter.

| | |
|---|---|
| Questions | 418 from 8 terms; 314 distinct |
| Reusable | yes 132, adapt 125, no 57 |
| Types | write-code 135, fill-in 67, diagram 36, explain 22, short-answer 19, other 14, debug 12, code-tracing 9 |
| Richest chapters | 17 Inheritance (47), 10 Dictionaries (37), 15 Classes and Methods (21), 9 Lists (18), 14 Classes and Functions (18) |
| Thin | 1, 7, 12, 13 and 18 have 5 or fewer each; 51 match no chapter (Pyro, threads, OpenGL, Subversion), 41 of them `no` |

What the agents found along the way:

- **Solutions are rare.** Spring 2011's Exam 2 solutions were in the Google Site
  crawl; a few exams and quizzes have `_soln` files. The same `exam01_soln.txt`
  (Spring 2004) and `quiz03_soln.txt` (a `square_list` email listing common wrong
  answers, good material for instructor notes) were copied into later terms' folders.
  Where an agent worked out an answer itself, it says so in `notes` — **those need
  Allen's review before being treated as solutions.**
- **Carried-over exams.** Several terms hold an older term's exam beside their own
  (`exam2`/`exam02`); these are cataloged as `exam02b` etc. or under their real term.
- **Errors in the originals:** `random.choose` (2004 fall exam 2), `__mult__` for
  `__mul__` (2008 exam 3), `d.get(word, 0)` for `d.get(c, 0)` (2013 exam 2), a
  syntax error in the 2004 `check_fermat` solution, among others — all in `notes`.
- **Lost dependencies:** Swampy, Pyro, `Poker.py`, `Sync.py`, `Shape.py`, NSFG
  handouts, missing figures (`exam3_trie.ps`, `pentatri.eps`). Some code survives in
  `archive/*/drive/code/` (`Sym.py`, `Subject.py`, `Observer.py`).
- **Conversion fixes.** Cataloging found four conversion bugs, all fixed in
  `to_text.py`: the exams' argument-less `\blank` (their fill-in lines vanished),
  `\noindent` swallowing the next group (`{\tt t}`), `{\tt *}` vanishing, and
  curly quotes inside code.
- **Student data that got through, now removed.** A student's folder with a
  hyphenated first name (`svn/<first-name>.<last>/`, 13 files) slipped past the
  `first.last` pattern, and the 2008 and 2011 `notes22.txt` held a demo schedule
  listing student teams by surname. The pattern now allows hyphens and the gather
  step redacts that schedule. The private repo's history was squashed to a single
  commit (`9875d79`) and force-pushed on 2026-11-06, so neither survives in any
  reachable commit. GitHub may keep the orphaned commits until its own cleanup;
  GitHub Support can purge them on request.

## Mining (step 4)

One subagent per chapter, against `bank/MINING_BRIEF.md`: each usable question is
updated to Python 3 and the 3rd edition, solved, **verified by a check script that
must pass** (`bank/check/chapNN_check.py`), given instructor notes, and sent to one of
`exam` (private bank), `activity` (in class), `quiz` (proposed for the public quiz)
or `drop`. Output per chapter: `bank/chapNN.md` for Allen's review.

**Allen's rules** (2026-11-06, recorded in the brief):

- Any tool the book has already introduced is fair game, in questions and solutions,
  and gets full credit. A question that needs something not yet taught moves to that
  later chapter, or gives it explicitly. The book's code never uses `while`,
  `continue`, `del` or `raise`; `random` first appears in Chapter 12, tuples in 11.
- State behaviour a grader would otherwise guess (duplicates, edge cases) in the
  question.
- When two items rest on the same idea, keep the better one.

**Chapters 9–11 (2026-11-06):** 71 catalog questions became 14 (Ch 9), 19 kept plus
7 dropped (Ch 10) and 14 (Ch 11) items, plus one moved to a new `bank/chap12.md`.
Decisions Allen made along the way:

- Ch 9: `only_reduplicated` uses the whole-word-doubled rule (`bonbon`, `tutu`);
  `t == sorted(t)` is full credit for `is_sorted`; `list_intersection` states its
  duplicates rule. The 2004 answer key for a debugging question gave the wrong
  reason; the item now uses the real Chapter 9 bug (emptying the caller's list).
- Ch 10: the strict `invert` (needs `raise`) and `count_duplicates` (too close to
  the book's exercises) dropped; memoized binomial moved to Ch 11 (tuple keys); the
  d20 dice moved to Ch 12 (`random`).
- Ch 11: both sorting questions allow `key=`; `gforce-pairs` dropped as overlapping
  `max-distance-pair`.
- **Public quiz:** of three proposals, two were accepted and added to
  `soln/quizzes.ipynb` (Ch 9: why aliasing is safe with strings; Ch 10: keys are like
  indices, values like elements). The Ch 11 `tuple_replace` question stays private as
  an activity.

**Chapters 2–6 (2026-11-06):** 68 catalog questions, mined the same way (five agents
in parallel; items needing a later chapter were written to `bank/moved/` and then
placed). Decisions:

- A question may introduce one small library function itself (the Ch 5 coin flip
  keeps `random.random`); a language feature not yet taught moves the item (Ch 6
  `is_alphabetical` → Ch 8 for string comparison). Recorded in the brief.
- Ch 3's review of Chapter 1–2 vocabulary split into `chap01.md` and `chap02.md` by
  where each term is introduced.
- Ch 4: the lost `pentatri` figure is reconstructed (pentagon with a triangle on each
  side), confirmed by Allen; `circle_star` accepts the exact and the visually
  corrected turn.
- Ch 5: Sierpinski stays dropped (it's in the book). `check_fermat` is not a 3e
  exercise, so it's an exam item.
- Four questions added to the public quiz: Ch 3 tracebacks, Ch 4 whose bug a
  precondition violation is, Ch 5 a base case never reached, Ch 6 printing vs.
  returning (`None`). The public quizzes now have 89 questions.

**Chapters 14–17 (2026-11-06):** 80 catalog questions; Chapter 17 (35) was mostly
Swampy, Pyro, threads and lost handouts, and kept only ideas that work on the book's
own classes. Decisions, now rules in the brief:

- The book never uses exceptions (`try`/`except`, `raise`), `while`, `continue`,
  `del`, `lambda` or `__call__`: a function that would raise returns `None` (Ch 14
  `add_vector`; Ch 15 time intervals).
- No explicit parent `__init__` calls (`Hand.__init__(self, …)`): a child's `__init__`
  sets every attribute itself, as the book's `Hand` does (Ch 17 BlackJack, Rummy,
  Go Fish, and the kangaroo question moved in from Ch 16).
- No class diagrams (the Ch 17 class-diagram activity dropped).
- Ch 15 `adjacency-bugs`: the mutable-default bug (not explained until Ch 17)
  swapped for a method defined without `self`.
- Two more public quiz questions: Ch 14 a parameter and an attribute with the same
  name; Ch 17 which `__init__` runs when `Hand` overrides `Deck`'s. The public
  quizzes now have 91 questions.

**Still to look for:** the 2021 Takeout archives of the classic Google Sites, which
weren't on this disk or the external drive (only a 2026 Blogger Takeout was). Allen
is searching Drive; a new Takeout of the converted sites is the fallback.

## Steps

1. **Gather.** Copy each source into `archive/<term>/<source>/` (for example,
   `archive/2013fa/svn/`), unchanged, with a `SOURCES.md` recording the original path
   or URL of each folder. Skip build products (`.aux`, `.log`, `.ps`, `.dvi`, `~`
   backups) and strip the `?attredirects=0` suffixes. Use the allowlist above, and log what was
   skipped. Where a term exists in more than one place (the external drive,
   `~/AllenDowneyCom`, `~/svn`, the Google Sites crawl), take the drive's copy as the
   base and add only files the others have that it lacks. Merge `svn.old/sd11s` into
   `svn/sd11s` after diffing them.
2. **Convert to text.** LaTeX to Markdown with `pandoc`; PDFs to text with
   `pdftotext`, only where no LaTeX source exists; HTML to Markdown. Keep the
   originals.
3. **Catalog.** One row per question in a CSV or JSON: term, source file, question
   type (multiple choice, code tracing, write code, explain), topic, matching 3rd
   edition chapter, whether there's a solution, and duplicates.
4. **Mine.** Sort each usable question into one of:
   - **public quiz additions**: multiple choice that fits the existing quizzes;
   - **private exam bank** (Task 17), in the same Markdown format as `quizzes.ipynb`
     so the Task 16 exporters work on it;
   - **in-class activities**: predict-the-output and find-the-bug questions;
   - **assignments and projects**: homework and project specs worth updating.
   Update each kept question to Python 3 and the 3rd edition, and run its code.
5. **Review.** Allen reviews each batch before it goes anywhere public or into the
   private bank.

Steps 1 to 3 are mechanical and can be done in one session. Step 4 is the real work,
best done a few chapters at a time.

## Open questions

- **Other terms:** with the drive, the archive covers Spring and Fall 2004, Spring
  2006 to 2008, Spring and Fall 2011, and Fall 2013. Nothing yet for 2005, 2009, 2010
  or 2012. Did those terms run, and are they anywhere?
- **Google Drive:** are the 2021 Takeout archives of the classic sites there?
- **Old public pages:** the 2004 to 2008 course pages and the 2013 Google Site are
  still public, quiz answers included in places. Leave them up?
