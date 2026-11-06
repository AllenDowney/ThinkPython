# Plan: Archive and mine the old Software Design materials

**Created:** 2026-11-06
**Board:** Task 18 in `PROJECT_BOARD.md` (feeds Task 17, teaching materials)
**Status:** Planning; sources surveyed, nothing copied yet

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
| Canvas (Olin) | — | — | — | — | — | **Not found**: no Software Design or Think Python quizzes in any course the API token can see |
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

## Where the archive lives

The archive holds exam and quiz answers, so it shouldn't go in this repository or
ThinkPythonSolutions, which are both public. Options:

1. **A new private repository**, e.g. `ThinkPythonTeaching`, nested here like
   ThinkPythonSolutions and gitignored by this repo. It's versioned and backed up, and
   it can later hold the private materials Task 17 produces.
2. **A local folder**, gitignored, e.g. `~/ThinkPython/teaching_archive/`. Simplest,
   but not backed up or shareable.

Recommendation: option 1, since Task 17's private exam bank and assignments need a
private home anyway.

## Steps

1. **Gather.** Copy each source into `archive/<term>/<source>/` (for example,
   `archive/2013fa/svn/`), unchanged, with a `SOURCES.md` recording the original path
   or URL of each folder. Skip build products (`.aux`, `.log`, `.ps`, `.dvi`, `~`
   backups) and strip the `?attredirects=0` suffixes. Merge `svn.old/sd11s` into
   `svn/sd11s` after diffing them. Find out where the Canvas material is.
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

- **Canvas:** which course had the Software Design quizzes? Nothing on canvas.olin.edu
  that the token can see, and the classes page lists no Software Design course on
  Canvas. Perhaps canvas.instructure.com (Free for Teacher), which needs its own token.
- **Other terms:** the classes page has nothing for Software Design in 2005 or 2009
  to 2010. Did those terms run, and are they anywhere?
- **Google Drive:** are the 2021 Takeout archives of the classic sites there?
- **The archive:** a private repository, or a local folder?
- **Old public pages:** the 2004 to 2008 course pages and the 2013 Google Site are
  still public, quiz answers included in places. Leave them up?
