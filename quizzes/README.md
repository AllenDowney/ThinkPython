# Think Python quizzes for your LMS

These are the quizzes for *Think Python*, 3rd edition, in formats you can import into a
learning management system:

* a formative quiz for each of Chapters 1 to 18 (3 to 6 questions each), and
* a summative quiz covering the whole book (21 questions).

Every question is multiple choice with four answers, and every answer comes with
feedback that explains why it is right or wrong. The answers are shuffled, either by
the LMS or in the file.

The questions are licensed, like the book, under
[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).

## Which file to use

| LMS | Folder | Format | Tested |
|---|---|---|---|
| **Canvas** | [`canvas/`](canvas/) | QTI 1.2 zip, one per quiz | Yes |
| **Brightspace (D2L)** | [`brightspace/`](brightspace/) or [`canvas/`](canvas/) | Question Library CSV, or the QTI 1.2 zips | No |
| **Moodle** | [`moodle/`](moodle/) | Moodle XML | No |

Each folder has one file per quiz (`chapter01` … `chapter18`, `summative`). `moodle/`
and `brightspace/` also have `all_quizzes`, with every question in one file.

The Moodle and Brightspace files follow those systems' documented formats but haven't
yet been imported into a real Moodle or Brightspace. If you try them, please
[open an issue](https://github.com/AllenDowney/ThinkPython/issues) and say whether they
worked.

## Importing

**Canvas.** In your course, go to **Settings → Import Course Content**, choose
**QTI .zip file**, upload one of the zips from `canvas/`, and click **Import**. Each zip
becomes an unpublished quiz worth one point per question. Import one zip at a time.
Canvas sometimes reports success without creating anything, so check the Quizzes page
afterwards.

**Moodle.** In your course, go to **Question bank → Import**, choose **Moodle XML
format**, and upload a file from `moodle/`. The questions go into a category named after
the quiz, under *Think Python*. Then add them to a quiz.

**Brightspace.** In a quiz or the Question Library, choose **Import → Upload a File**
and upload a CSV from `brightspace/`. Alternatively, use **Import/Export/Copy
Components** with a QTI zip from `canvas/`.

## Where these come from

The quizzes are written in a Markdown format in the solutions repository,
[ThinkPythonSolutions](https://github.com/AllenDowney/ThinkPythonSolutions), and these
files are generated from it. Please don't edit them here; corrections should go to the
source.
