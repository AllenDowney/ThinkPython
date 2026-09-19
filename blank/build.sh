# Build the blank notebooks

# copy notebooks from soln

cp ../ThinkPythonSolutions/soln/chap[01][0-9]*.ipynb .

# remove the solutions and code from all cells (unless they have the `keep` tag)
python prep_notebooks.py

# commit the changes
git add chap*.ipynb
git commit -m "Updating the blank notebooks"
git push
