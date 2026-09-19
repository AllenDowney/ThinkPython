import nbformat as nbf
from glob import glob

# Collect a list of all notebooks in the content folder
filenames = glob("chap*.ipynb")

text = '# Solution'
replacement = ''

# Search through each notebook
for filename in sorted(filenames):
    print('Removing solutions from', filename)
    ntbk = nbf.read(filename, nbf.NO_CONVERT)

    for cell in ntbk.cells:
        # remove tags
        if 'tags' in cell['metadata']:
            tags = cell['metadata']['tags']
            cell['metadata']['tags'] = []
        else:
            tags = []

        # remove output
        if 'outputs' in cell:
            cell['outputs'] = []

        # remove all code except from cells with the `keep` tag
        if cell['cell_type'] == 'code' and 'keep' not in tags:
            cell['source'] = ''


    nbf.write(ntbk, filename)
