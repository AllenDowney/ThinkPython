import nbformat as nbf
from glob import glob

# Collect a list of all notebooks in the content folder
notebooks = glob("chap*.ipynb")

text = '# Solution'
replacement = '# Solution goes here'

# Search through each notebook
for ipath in notebooks:
    ntbk = nbf.read(ipath, nbf.NO_CONVERT)

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

        # remove solutions
        if cell['source'].startswith(text):
            cell['source'] = replacement

        # remove solutions
        if 'solution' in tags:
            cell['source'] = replacement

        # add label
        for tag in tags:
            if tag.startswith('chapter') or tag.startswith('section'):
                label = f'({tag})=\n'
                cell['source'] = label + cell['source']

    nbf.write(ntbk, ipath)
