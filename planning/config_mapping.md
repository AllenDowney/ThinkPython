# Configuration Mapping: JB 1.x → JB 2.0

> **Note:** This is reference material for a **deferred migration project** (as of Jan 12, 2026).  
> JB 2.0 migration is on hold due to too many unknowns. See `plan.md` for details.  
> Keep this file for future reference if/when migration becomes necessary.

---

## Mapping _config.yml + _toc.yml → myst.yml

### ✅ Direct Mappings (Confirmed from Examples)

| JB 1.x (_config.yml) | JB 2.0 (myst.yml) | Notes |
|---------------------|-------------------|-------|
| `title: Think Python` | `project.title: Think Python` | Also duplicated in `site.title` |
| `author: Allen B. Downey` | `project.authors: [{name: Allen B. Downey}]` | Array format in JB 2.0 |
| `repository.url: https://...` | `project.github: https://...` | Simplified to just github URL |
| `html.use_repository_button: true` | (implicit with github URL?) | Need to verify |
| N/A | `site.template: book-theme` | Required in JB 2.0 |
| N/A | `site.options.logo_text: Think Python` | Used in examples |

### 📋 TOC Mapping

**JB 1.x (_toc.yml):**
```yaml
format: jb-book
root: index
parts:
- caption: Front Matter
  chapters:
  - file: chap00
- caption: Chapters
  numbered: True
  chapters:
    - file: chap01
    ...
- caption: End Matter
  chapters:
  - file: blank
```

**JB 2.0 (myst.yml):**
```yaml
project:
  toc:
    - file: index.md
    - file: chap00.ipynb
      title: Front Matter
    - file: chap01.ipynb
    - file: chap02.ipynb
    ... (all 19 chapters)
    - file: blank.md
      title: Blank Notebooks
```

**Issues to Resolve:**
- ❓ How to handle parts/captions in JB 2.0?
- ❓ How to enable chapter numbering?
- ❓ Can we group chapters into sections?

### ❓ Unclear/Research Needed

| JB 1.x Setting | JB 2.0 Equivalent? | Status |
|----------------|-------------------|--------|
| `execute.execute_notebooks: 'off'` | `project.execute: {}`? | Unknown - not in examples |
| `parse.myst_enable_extensions: [amsmath, dollarmath, ...]` | `project.myst: {}`? | Unknown - not in examples |
| `sphinx.config.mathjax_path: ...` | `project.math: {}`? | Unknown |
| `sphinx.config.mathjax_config: ...` | `project.math: {}`? | Unknown |
| `html.extra_footer: ...` | `site.options.footer: ...`? | Unknown |
| `latex.latex_documents.targetname: book.tex` | ??? | May not be needed for HTML-only |

### Current MyST Extensions to Migrate
From _config.yml:
- amsmath
- colon_fence
- deflist
- dollarmath
- fieldlist
- html_admonition
- html_image
- linkify
- replacements
- smartquotes
- strikethrough
- substitution
- tasklist

### Custom HTML Footer (CC License)
Current in _config.yml:
```yaml
html:
  extra_footer: |
    <div style="text-align: left;">
      <a rel="license" href="https://creativecommons.org/licenses/by-nc-sa/4.0/">
        <img alt="Creative Commons License" style="border-width:0"
             src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" />
      </a>
      <br />
      This work is licensed under a
      <a rel="license" href="https://creativecommons.org/licenses/by-nc-sa/4.0/">
        Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License
      </a>.
    </div>
```

Need to find equivalent in JB 2.0.

## Proposed Initial myst.yml (Basic Version)

```yaml
# See docs at: https://mystmd.org/guide/frontmatter
version: 1

project:
  title: Think Python
  authors:
    - name: Allen B. Downey
  github: https://github.com/AllenDowney/ThinkPython/tree/v3
  # license: CC-BY-NC-SA-4.0  # May be supported
  
  toc:
    - file: index.md
    - file: chap00.ipynb
      title: "Preface"
    - file: chap01.ipynb
      title: "Chapter 1: Programming as a way of thinking"
    - file: chap02.ipynb
      title: "Chapter 2: Variables and Statements"
    - file: chap03.ipynb
      title: "Chapter 3: Functions"
    - file: chap04.ipynb
      title: "Chapter 4: Functions and Interfaces"
    - file: chap05.ipynb
      title: "Chapter 5: Conditionals and Recursion"
    - file: chap06.ipynb
      title: "Chapter 6: Return Values"
    - file: chap07.ipynb
      title: "Chapter 7: Iteration and Search"
    - file: chap08.ipynb
      title: "Chapter 8: Strings and Regular Expressions"
    - file: chap09.ipynb
      title: "Chapter 9: Lists"
    - file: chap10.ipynb
      title: "Chapter 10: Dictionaries"
    - file: chap11.ipynb
      title: "Chapter 11: Tuples"
    - file: chap12.ipynb
      title: "Chapter 12: Text Analysis and Generation"
    - file: chap13.ipynb
      title: "Chapter 13: Files and Databases"
    - file: chap14.ipynb
      title: "Chapter 14: Classes and Functions"
    - file: chap15.ipynb
      title: "Chapter 15: Classes and Methods"
    - file: chap16.ipynb
      title: "Chapter 16: Classes and Objects"
    - file: chap17.ipynb
      title: "Chapter 17: Inheritance"
    - file: chap18.ipynb
      title: "Chapter 18: Python Extras"
    - file: chap19.ipynb
      title: "Chapter 19: Final Thoughts"
    - file: blank.md
      title: "Blank Notebooks"

site:
  template: book-theme
  title: Think Python
  options:
    logo_text: Think Python

# TODO: Research how to add these in JB 2.0:
# - MyST extensions (amsmath, dollarmath, etc.)
# - execute_notebooks: 'off'
# - Custom HTML footer with CC license
# - MathJax configuration
# - Repository button
```

## Next Steps

1. Create jb2/ directory
2. Copy content files from jb/ to jb2/
3. Create initial myst.yml (basic version above)
4. Test build and see what works/what errors we get
5. Iteratively add missing configurations based on:
   - Build errors/warnings
   - Documentation research
   - Trial and error
6. Document findings for future reference

## Build Process Changes

**Old (JB 1.x):**
```bash
jb build .
```

**New (JB 2.0) - from other projects:**
```bash
jupyter book build --html --strict
```

**For GitHub Pages:**
```bash
BASE_URL=/ThinkPython/ jupyter book build --html --strict
touch _build/html/.nojekyll
ghp-import -n -p -f _build/html
```

