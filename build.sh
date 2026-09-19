# copy the current version of the support files

cp ThinkPythonSolutions/soln/thinkpython.py .
cp ThinkPythonSolutions/soln/diagram.py .
cp ThinkPythonSolutions/soln/structshape.py .
cp ThinkPythonSolutions/soln/words.txt .
cp ThinkPythonSolutions/soln/photos.zip .

rsvg-convert jupyturtle_pie.svg -o jupyturtle_pie.png
rsvg-convert jupyturtle_flower.svg -o jupyturtle_flower.png
git add jupyturtle_pie.png jupyturtle_flower.png

# commit the changes
git add thinkpython.py diagram.py structshape.py words.txt photos.zip
git commit -m "Updating the support files"
git push
