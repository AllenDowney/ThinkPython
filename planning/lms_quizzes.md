# Plan: Quizzes that LMSs can import

**Created:** 2026-11-06
**Board:** Task 16 in `PROJECT_BOARD.md`
**Status:** Steps 1 and 2 done; QTI 1.2 exporter written and tested on Canvas 2026-11-06. Next: Moodle XML and Brightspace CSV exporters, then publishing

## Goal

An instructor using *Think Python* should be able to download the quizzes and import
them into their LMS (Canvas, Moodle, Brightspace or Blackboard) without retyping
anything. Each choice should keep its rationale, shown as feedback.

## Constraint: the source format stays

`ThinkPythonSolutions/soln/quizzes.ipynb` is the source. It is Markdown in O'Reilly's
quiz format, which works with O'Reilly's tooling, so it stays as it is. Every LMS
format is generated from it, never edited by hand.

Each question has the same shape:

- `# Title` (`Chapter N`, or `Think Python` for the summative quiz) and `## Quiz Type`
  (`Formative` or `Summative`) open a quiz.
- `### Question` is followed by the prompt, which may contain code blocks, inline
  code and (once) `$…$` math.
- Four choices follow, `- [ ]` / `- [X]`. The correct one is always last.
- `### Rationale` gives four bullets, one per choice, in the same order.

There are 18 formative quizzes (62 questions, 3 to 6 per chapter) and one summative
quiz (21 questions). An empty template question at the end was removed 2026-11-06.

`soln/quizzes/quizzes.md` is a copy of the same text without the jupytext region
markers. It was made for the February 2026 Google Forms work. The quizzes are not
generated from it.

## What exists, and why it doesn't import

| File | Made | Format | Problem |
|---|---|---|---|
| `soln/quizzes_qti.zip` | 2025-06 | QTI 2.1, 84 items in one package | Well-formed XML but not valid QTI 2.1: `responseDeclaration` comes after `itemBody`, there is no `responseProcessing`, choice text is raw Markdown (literal backticks), and there are no rationales |
| `soln/quizzes/Chapter_*_qti.zip`, `Summative_Quiz_qti.zip`, `quizzes_qti.zip` | 2026-02 | QTI 2.1, one package per quiz | **Not well-formed XML.** Every item uses `xsi:schemaLocation` without declaring the `xsi` namespace, so any XML parser rejects it before it reaches the QTI checks (`xmllint`: "Namespace prefix xsi for schemaLocation on assessmentItem is not defined"). The rationales are lumped into one feedback block, inside nested `<p><p>` |
| `soln/ThinkPythonQuizzesBrightspace.csv` | 2025-08 | Brightspace question CSV | Not tested here. Not generated from the source, so it has drifted from any fixes since |
| `soln/quizzes/create_google_quiz.py` and friends | 2026-02 | Google Forms via API | Works. Not an LMS import, but `parse_quizzes.py` already turns the source into JSON, and the new exporters can start from it |

Both QTI attempts used QTI 2.1, which is the less-supported version (see below).

## Which LMS imports what

| LMS | Imports | Best target |
|---|---|---|
| **Canvas** | QTI 1.2 and 2.x. Classic Quizzes reliably takes only 1.2. Canvas exports only 1.2 and recommends 1.2 for import. It creates new quizzes only and fails silently on bad files | **QTI 1.2** |
| **Moodle** | Moodle XML (recommended, keeps per-answer feedback), GIFT, Aiken. QTI needs a plugin on most sites | **Moodle XML** |
| **Brightspace (D2L)** | QTI 1.2, IMS Common Cartridge 1.0 to 1.3, and its own CSV template. QTI 2.1 support is not documented | **QTI 1.2**, with CSV as a fallback |
| **Blackboard** | QTI 2.1 packages as question pools in the Original course view; Ultra goes through an Original-to-Ultra pool import. Unsupported question types are dropped | Needs testing; QTI 1.2 in a Common Cartridge is the candidate |

So **QTI 1.2 covers Canvas and Brightspace, and Moodle XML covers Moodle.** Those two
generated files reach the three most common LMSs. Blackboard is the open question.

**IMS Common Cartridge**, a zip that wraps QTI 1.2 assessments, is the one package
that all four LMSs advertise. It is worth testing as a single download, but it is a
course-content import (it brings in "quizzes" as course items), not a question-bank
import, so it is a second target, not the first.

### Tools for writing them

- **`text2qti`** (Geoffrey Poore, on PyPI) converts Markdown-based plain text to QTI
  1.2 zips aimed at Canvas. It handles Markdown to HTML, code, per-choice feedback and
  LaTeX math. Its input is close to our format (it marks the correct answer with `*`
  rather than `[X]`), so one path is: our source → `text2qti` text → QTI 1.2. The risk
  is that its math support wants an institutional LaTeX rendering URL; we have one
  `$…$` question and can rewrite it in plain text.
- **Write the XML ourselves** from `parse_quizzes.py`'s JSON. QTI 1.2 multiple choice
  and Moodle XML are both small, well-documented formats; a template per question is
  about 40 lines of Python each. This keeps one parser and no new dependency.
- **Moodle XML vs GIFT:** both are Moodle-only. Moodle XML is the one Moodle
  recommends, keeps per-answer feedback and takes HTML, so code blocks survive. GIFT is
  a text format that's easy to read but needs escaping for `{}=~#:` characters, which
  our Python code is full of.

**Recommendation:** write our own QTI 1.2 and Moodle XML exporters from the existing
JSON, and use `text2qti` as a reference to check our QTI 1.2 against. Validate every
generated file with `xmllint` in `make tests`, so the February failure can't recur
silently.

## Steps

1. **Review the questions** for typos and errors (in progress; findings below). Fix
   them in `soln/quizzes.ipynb` through jupytext, the same as a chapter.
2. **Decide the open questions** below.
3. **Exporters:** `quizzes/export_qti12.py`, `quizzes/export_moodle.py` and
   `quizzes/export_brightspace.py` reading the parsed JSON. Each choice gets its own rationale as feedback. Code blocks become
   `<pre><code>`, inline code becomes `<code>`. One package per quiz, plus one with
   everything.
4. **Validate:** `xmllint --noout` on every generated file, in `make tests`.
5. **Test imports** into Canvas (the only LMS we can test on now). Check
   that the code renders, the right answer is marked and the feedback shows.
6. **Publish:** decide where instructors find them (below), and retire the broken
   zips and the hand-made CSV.

## Canvas test results (2026-11-06)

Imported through the API (content migration, `qti_converter`) into the sandbox course
629 on Olin's Canvas, then read back what was created:

| Package | Classic Quizzes | New Quizzes |
|---|---|---|
| `soln/quizzes_qti.zip` (2025, QTI 2.1) | migration "completed", 0 issues, **nothing created** | same |
| `soln/quizzes/Chapter_1_qti.zip` (2026, QTI 2.1) | migration "completed", 0 issues, **nothing created** | same |
| Control: Ch 1 Q1 through `text2qti` (QTI 1.2) | **quiz created**: code as `<code>`, the right answer marked, each choice's rationale as its feedback | setting ignored; made a classic quiz |
| `export_text2qti.py`: Chapters 3 and 8, summative | **all created**, every question present; code blocks keep their indentation; `$` in the regex patterns survives; answers shuffled; 1 point each; unpublished | not tested |

So the old zips fail silently, exactly as Canvas's docs warn, and QTI 1.2 in the
shape `text2qti` writes imports cleanly. The New Quizzes path couldn't be tested:
`settings[import_quizzes_next]` was ignored, presumably because New Quizzes is not
enabled for course 629.

So the Canvas/Brightspace exporter takes the `text2qti` route (decided 2026-11-06):
`soln/quizzes/export_text2qti.py` writes each quiz as `text2qti` text from the parsed
JSON and runs `text2qti`, giving 19 packages in `soln/quizzes/build/qti12/` (ignored).
All the generated XML passes `xmllint`. `soln/quizzes/canvas_import.py` runs the
import test against the sandbox course.

Two things the exporter has to do that the source doesn't:

- **Shuffle the answers.** The correct answer is always last in the source, so
  without `Shuffle answers: true` every answer in Canvas would be (d).
- **Keep code indentation.** `parse_quizzes.py` used to strip every line, which
  flattened the code in every question (and in the Google Forms quizzes built from
  it, which still have flattened code). Fixed 2026-11-06.

Smart quotes: `text2qti` curls the quotes and apostrophes in prose (`can’t`), but not
inside code.

## Decisions (2026-11-06)

- **Downloads live in `quizzes/` in ThinkPython**, next to `chapters/`, rebuilt by
  `update.py` like the other targets and linked from the README and the website.
- **Brightspace CSV: generate it too**, as a third exporter beside QTI 1.2 and Moodle
  XML. The hand-made `soln/ThinkPythonQuizzesBrightspace.csv` is retired once the
  generated one exists.
- **Testing: Canvas only** for now. Moodle, Brightspace and Blackboard imports are
  untested until someone with access tries them; the README should say so.

## Open questions

- ~~**`"chaptertitle"`:**~~ resolved 2026-11-06. It was not an O'Reilly placeholder;
  the 88 references in the summative rationales now give the real chapter titles.
- ~~**Where do the downloads live?**~~ `quizzes/` in ThinkPython (see Decisions).
- ~~**Brightspace CSV:**~~ generate it (see Decisions).
- **Moodle, Brightspace, Blackboard:** no test access. Worth asking readers who teach
  with them, once the files are published.
- ~~**The empty template question**~~ at the end of the summative quiz: removed
  2026-11-06.

## Review findings (step 1)

Checked 2026-11-06, all 84 questions. The code claims were run in Python 3.

**All of these are applied** in `soln/quizzes.ipynb`, reviewed by Allen and committed
2026-11-06. The fixes for the first table:

- **Ch 7 `check`:** the two `letter` choices are now "all of the letters in `letters`
  appear in `word`" and "the first letter of `word` does not appear in `letters`" (the
  misconception that the loop stops early), with new rationales.
- **Ch 18 `Game`:** `score` → `scores`.
- **Ch 13:** the choice is now `''.join(['/home/dinsdale/photos', 'mar-2023/photo1.jpg'])`,
  which runs and matches its rationale.
- **Summative, lowercase:** the prompt is now "If `s` is a string…", and every `str` is `s`.
- **Summative, reverse:** both rationales now say `reversed` returns an iterator.
- **Ch 10:** `d3` → `d2`.
- **Summative, `Day`:** keeps `print`, since the point is that `print` invokes
  `__str__`; the choices are now written as displayed output, without quotes.
- **"logic error"** is now "semantic error" in both summative questions that used it.

### Wrong or ambiguous answers

| Quiz | Question | Problem |
|---|---|---|
| Ch 7 | `check(word, letters)` | Choices 2 and 3 say `letter` instead of `letters`. Once that's fixed, choice 3 ("none of the letters in `word` appear in `letters`") is **logically the same as the correct answer**, so the question has two right answers |
| Ch 18 | `Game` default-argument | The code says `self.scores = score`, so `Game()` raises `NameError`. Should be `scores` |
| Ch 13 | absolute path | Choice 1, `''.join('/home/…', 'mar-2023/…')`, raises `TypeError` (`join` takes one argument). The rationale says it "does not put a slash between the directories" |
| Summative | lowercase string | Uses `str` as the variable. `str.lower()` with the built-in raises `TypeError`, and the book warns against shadowing built-ins. Suggest `s` |
| Summative | reverse in place | Rationales 1 and 2 say `reversed` "creates a new list"; it returns an iterator. Rationale 2 also says `reverse(t)` for `reversed(t)` |
| Ch 10 | dictionary as key | Choice 1 says "a key in `d3`"; there is no `d3`, it should be `d2` |

### Typos

| Quiz | Where | Fix |
|---|---|---|
| Ch 1 | Q2 heading | `### Rationales` → `### Rationale` (it may also trip a parser) |
| Ch 1 | Q2 rationale 4 | "first operator is a string" → "first operand" |
| Ch 7 | Q1 prompt | "contains with `'A'`" → "contains `'A'`"; "-- What's" → "-- what's" |
| Ch 7 | Q2 rationale 3 | "to`x`" → "to `x`" |
| Ch 10 | Q3 rationales 2, 3 | "`KeyError.`" and "`ValueError.`" → period outside the backticks |
| Ch 11 | Q1 rationales 2, 3 | "value if this expression" → "of"; "with on element" → "with one element" |
| Ch 15 | Q1 choices 2, 3 | "one arguments" → "one argument"; "two argument" → "two arguments" |
| Ch 16 | Q2 rationale 1 | "with a two underscore characters" → "with two underscore characters" |
| Ch 18 | Q1 rationale 2 | "When the set is create" → "created" |
| Ch 18 | Q5 rationale 3 | "the `append` method add" → "adds" |
| Summative | lower_upper rationale 2 | "it select" → "it selects" |
| Summative | regex rationale 4 | "at the beginning `'f'`" → "at the beginning, `'f'`" |
| Summative | `round` | "round off to three decimal places" → "rounded" |

### Smaller issues

- **Question mark:** Ch 7 Q2 ("…assigned a value."), Ch 17 Q1 ("…class variables.") and Ch 17 Q2 ("…`==` operator.") are questions that end with a period.
- **Ch 18 Q2:** "value of counter" should be "value of `counter`", and rationale 4 says "elements of the list" for a tuple.
- **Ch 1 Q1:** the choice `string` was meant to be the string type, not a trick; it is now `str`, and the rationale says "`str` values contain a sequence of characters".
- **Ch 15 Q2:** begins "Suppose `time` is a `Time` object", copied from Q1, but the question never uses `time`.
- **Ch 8 Q2:** the choices aren't in code format, unlike every other code choice.
- **Ch 8 Q1:** rationale 4 is a fragment ("Because when we compare…").
- **Ch 12 Q1:** choice 3 has no final period, unlike the others.
- **Ch 17 Q1:** rationale 1 has no final period.
- **Summative, `Day` class:** the program prints `Today is Wednesday`, without quotes; the correct choice shows `'Today is Wednesday'`.
- **Summative, `compare`:** says "logic error", while the Ch 2 quiz and the book say "semantic error".
- **Ch 1 Q4:** the prompt has `$8 ÷ 2(2+2)$`, the only LaTeX in the file; the exporters can't count on the LMS rendering it. Plain text or code formatting would do.
- **Doubled spaces:** in Ch 2 Q2 ("`**`,  is"), Ch 4 Q3 (`arc(radius,  360)`), summative `compute` ("not  `word2`") and the `namedtuple` rationales ("the  bracket").
- **Empty code cell** before the summative quiz, and the empty template question at the end.
