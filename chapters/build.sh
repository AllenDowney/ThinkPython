# Build the notebook folder and zip file

# copy notebooks from soln

cp ../ThinkPythonSolutions/soln/chap[01][0-9]*.ipynb .
cp ../ThinkPythonSolutions/soln/jupyter_intro.ipynb .
cp ../ThinkPythonSolutions/soln/thinkpython.py .
cp ../ThinkPythonSolutions/soln/diagram.py .
cp ../ThinkPythonSolutions/soln/structshape.py .
cp ../ThinkPythonSolutions/soln/words.txt .
cp ../ThinkPythonSolutions/soln/photos.zip .

# remove the solutions
python prep_notebooks.py

# pip install pytest nbmake

# run nbmake
# TODO: can we get the %%expect magic to work?
# pytest --nbmake chap*.ipynb

# commit the changes
git add jupyter_intro.ipynb
git add chap*.ipynb
git commit -m "Updating the notebooks"

# build the zip file
cd ../..; zip -r ThinkPythonNotebooks.zip \
    ThinkPython/chapters/jupyter_intro.ipynb \
    ThinkPython/chapters/chap*.ipynb \
    ThinkPython/thinkpython.py \
    ThinkPython/diagram.py \
    ThinkPython/structshape.py \
    ThinkPython/words.txt \
    ThinkPython/photos.zip

# add and commit it
mv ThinkPythonNotebooks.zip ThinkPython
cd ThinkPython

git add ThinkPythonNotebooks.zip
git commit -m "Updating the zip file"

git push
