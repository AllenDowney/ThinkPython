# Build the LMS quiz downloads from the solutions repo.
#
# Source: ../ThinkPythonSolutions/soln/quizzes.ipynb (O'Reilly quiz format), which
# update.py has already parsed into soln/quizzes/parsed_quizzes.json and committed.
# Output: canvas/ (QTI 1.2, also for Brightspace), moodle/ (Moodle XML),
#         brightspace/ (Brightspace CSV). README.md here is written by hand.
# Needs markdown and text2qti (ThinkPythonSolutions/requirements-dev.txt).
# See planning/lms_quizzes.md.

set -e

SRC=../ThinkPythonSolutions/soln/quizzes
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

python $SRC/export_text2qti.py "$TMP/qti12"
python $SRC/export_lms.py "$TMP"

rm -rf canvas moodle brightspace
mkdir canvas
cp "$TMP"/qti12/*.zip canvas/
cp -r "$TMP"/moodle "$TMP"/brightspace .

# commit the changes
git add README.md build.sh canvas moodle brightspace
git commit -m "Updating the quizzes" || echo "quizzes unchanged"
git push
