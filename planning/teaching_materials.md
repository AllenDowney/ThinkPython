# Plan: Teaching materials for *Think Python*

**Created:** 2026-11-06
**Board:** Task 17 in `PROJECT_BOARD.md`
**Status:** Planning; nothing built yet

## Goal

Teachers often ask whether there is additional material for the book. The aim is that
an instructor adopting *Think Python* finds, in one place, what they need to plan a
course, teach each class, and assess students, without having to build it
themselves.

## What exists today

| Material | Where | Notes |
|---|---|---|
| Solution notebooks | the website, `ThinkPythonSolutions` | **Public**, so they can't be used for grading |
| Student notebooks, one Colab link per chapter | `chapters/`, the website | Solutions blanked |
| Blank notebooks for follow-along live coding | `blank/`, the website | Setup and diagram code kept in every chapter since 2026-11-06 |
| Quizzes: 18 formative, 1 summative, 83 questions | `quizzes/` (Canvas, Moodle, Brightspace), website page | Task 16. **The answers are public** |
| 81 exercises, plus "Ask a virtual assistant" prompts | in each chapter | Answers public |
| "Resources for Teachers" in the Preface | `soln/chap00` | Points to the solutions, says quizzes are "available on request", and links *Teaching and Learning with Jupyter* and Carpentries instructor training |

The pattern: there's plenty of material for **learning**, but nothing for **assessment**
that students can't look up, and nothing that helps a teacher **plan** or **run** a class.

## What teachers probably want

These are guesses, to check against real requests (step 1). They're grouped by what
the teacher is doing, and each gets a rough value and cost.

### Planning a course

- **Syllabus templates:** a 14-week semester, a 10-week quarter and an intensive
  (bootcamp or summer) version, each mapping chapters to weeks, with the quizzes and
  assignments placed. Cheap, and probably the most common question after "are there
  slides?".
- **Pacing guide and chapter dependencies:** which chapters can be skipped or
  reordered (for example, Chapter 4's turtle graphics, Chapter 13's files and
  databases, the Chapter 12 text-generation case study), and roughly how much class
  time each takes. A small diagram plus a table.
- **Learning objectives per chapter:** 3 to 6 "after this chapter, students can…"
  statements. Teachers need them for syllabi and accreditation, and they give the
  quizzes and any new assessments something to align to.

### Teaching a class

- **Slides per chapter.** The most-requested item, and the most expensive. Options:
  1. Generate them from the chapter notebooks (Jupyter slideshow metadata with
     reveal.js via `nbconvert`, or Quarto). Stays in sync with the book and the code
     runs, but notebook prose makes poor slides without real editing.
  2. Write separate decks (Markdown to reveal.js or Quarto, or Google Slides /
     PowerPoint so teachers can edit them). Better slides, but 18 decks to write and
     keep in sync.
  3. Pilot one chapter both ways before committing.
  Teachers usually want to edit slides, which argues for an editable format
  (PowerPoint or Google Slides) as at least one output.
- **Instructor notes per chapter:** where students get stuck, common misconceptions
  (for example, `=` vs `==`, aliasing in Chapter 9, mutable default arguments in
  Chapter 18), suggested live-coding demos using the blank notebooks, timing and
  discussion questions. High value per page, and something only the author can write
  well.
- **In-class activities:** predict-the-output questions, debugging hunts (the
  `%%expect` cells already have good material), Parsons problems (reordering
  scrambled lines of code) and pair-programming exercises. Short, printable, one or
  two per chapter.

### Assessing students

- **Graded assignments with private solutions.** Because the book's exercise
  solutions are public, teachers need new problem sets. Each would come with an
  autograder so a teacher can actually use it at scale: `otter-grader` or `nbgrader`
  for notebooks, or Gradescope's autograder. This is the most valuable item for
  someone teaching a large course, and the most work.
- **A larger, private question bank** for exams: code tracing, "explain in plain
  English", find the bug, and Parsons problems, beyond the 83 public quiz questions.
  It could reuse the quiz pipeline from Task 16 (same source format, same LMS
  exports), kept in a private repository.
- **Projects:** 3 to 5 multi-week project specifications with rubrics, building on
  the case studies (for example, the Markov text generator in Chapter 12 or the card
  games in Chapter 17).

### Other

- **AI guidance.** Every chapter has "Ask a virtual assistant" prompts, so the book
  already takes a position. A short guide for teachers: suggested course policies,
  assignments that still work when students have AI help, and how to use the prompts
  in class.
- **Videos:** short screencasts per chapter. Expensive; only worth it if teachers
  ask.
- **An LMS course shell:** a Common Cartridge with the syllabus, quizzes and
  assignments, so a Canvas or Moodle course can be set up in one import. Only once
  the pieces above exist.

**Allen's view (2026-11-06):** slides, private assignments, course planning and
instructor notes would all be valuable; none of the four is a low priority. The order
below is by cost, not value: course planning is cheapest, so it goes first, while
slides and assignments start as pilots.

## Constraints and decisions to make

- **Public vs. private.** Anything for grading has to be private: a private
  repository, plus a way to give access to verified instructors (a request form, or
  GitHub team access on request). This needs a decision before any assessment
  material is written, and it changes the Preface's "available on request" story.
- **O'Reilly.** Publishers often run an instructor-resources program for adopted
  textbooks. Worth asking whether O'Reilly has one for this book, and whether it
  would host the private materials.
- **Where it all lives.** The website's Quizzes page could grow into a "For
  Instructors" page that links everything, and the Preface's "Resources for
  Teachers" could point to it.
- **Maintenance.** Every generated item should come from a source in the repos, as
  with the quizzes, so a fix to the book flows through. Hand-made decks drift.

## Steps

1. **Find out what teachers actually ask for.** Go through past emails from teachers
   and list what they requested. Then add a short "what would help you?" link (a
   form) to the Quizzes page, and later to the Instructors page.
2. **Cheap, high-value pieces first:** learning objectives per chapter, a pacing
   guide with chapter dependencies, and syllabus templates. Publish them on a "For
   Instructors" page that absorbs the Quizzes page.
3. **Decide public vs. private**, and how instructors get access.
4. **Pilot slides for one chapter** (Chapter 2, say) in the two approaches above, and
   ask a few teachers which they'd use.
5. **Pilot one graded assignment** with a private solution and an autograder.
6. Then scale up whichever pilots work, in the order teachers ask for them.

## Open questions

- What have teachers actually asked for? (Step 1 answers this.)
- Slides: generated from the notebooks, or separate and editable?
- Which autograder: `otter-grader`, `nbgrader`, or Gradescope?
- Private materials: our own private repository, or O'Reilly's instructor resources?
- Who else could help write instructor notes or assignments, such as teachers already
  using the book?
