# Task 2.2: Potential Issues Analysis

> **Note:** This is reference material for a **deferred migration project** (as of Jan 12, 2026).  
> JB 2.0 migration is on hold due to too many unknowns (see Risk Summary below).  
> Keep this file for future reference if/when migration becomes necessary.

---

## Current Workflow Analysis

### Build Process (build.sh)
```bash
# 1. Copy notebooks from ThinkPythonSolutions
cp ../ThinkPythonSolutions/soln/chap[01][0-9]*.ipynb .

# 2. Process notebooks (remove solutions, add labels)
python prep_notebooks.py

# 3. Build with JB 1.x
jb build .

# 4. Deploy to GitHub Pages
ghp-import -n -p -f _build/html
```

### prep_notebooks.py Functionality
- Removes solution code (cells starting with `# Solution` or tagged 'solution')
- Removes `%%expect` cell magic
- Adds MyST reference labels for cells tagged with 'chapter' or 'section'
  - Format: `(chapter_programming)=` or `(section_name)=`

---

## Issue Categories

### 🟢 LOW RISK - Should Work Without Changes

#### 1. **prep_notebooks.py Script**
- **Status:** ✅ Should work unchanged
- **Reason:** 
  - Script only manipulates notebook JSON structure
  - MyST reference labels `(label)=` are standard MyST syntax
  - JB 2.0 still supports MyST markdown in notebooks
- **Action:** Test to confirm, but expect no changes needed

#### 2. **ghp-import Deployment**
- **Status:** ✅ Should work unchanged
- **Reason:**
  - BayesFertility and HALE use same `ghp-import -n -p -f _build/html`
  - Output directory remains `_build/html`
  - Only difference: may need `.nojekyll` file (already done in examples)
- **Action:** Add `touch _build/html/.nojekyll` to build script

#### 3. **Notebook Content**
- **Status:** ✅ Should work unchanged
- **Reason:**
  - Notebooks contain standard markdown and code cells
  - MyST syntax in cells is standard
  - No special JB 1.x-specific syntax observed
- **Action:** None needed

---

### 🟡 MEDIUM RISK - May Need Configuration Research

#### 4. **MyST Extensions**
- **Current:** 13 extensions enabled in `parse.myst_enable_extensions`
  - amsmath, colon_fence, deflist, dollarmath, fieldlist
  - html_admonition, html_image, linkify, replacements
  - smartquotes, strikethrough, substitution, tasklist
- **Issue:** Unknown how to configure these in myst.yml
- **Impact:** If not configured, some syntax may not render correctly
  - Admonitions might not work
  - Math notation might not work
  - Smart quotes might not work
  - Task lists might not work
- **Search Required:** ✓ High priority
  - Look for: `project.myst`, `project.jupyter`, or similar in myst.yml
  - May be enabled by default in JB 2.0
  - May need to use MyST CLI options
- **Workaround:** Test with basic config first, see what breaks

#### 5. **MathJax Configuration**
- **Current:** Custom MathJax path and tex2jax config
  ```yaml
  mathjax_path: https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js
  mathjax_config:
    tex2jax:
      inlineMath: [["$","$"], ["\\(", "\\)"]]
  ```
- **Issue:** Unknown how to configure in myst.yml
- **Impact:** Math rendering might use different settings
  - Note: Quick check shows book may not use much math notation
  - Low actual impact if math isn't heavily used
- **Search Required:** ✓ Medium priority
  - Look for: math configuration in JB 2.0
- **Workaround:** May work with defaults

#### 6. **Execute Notebooks Setting**
- **Current:** `execute_notebooks: 'off'`
- **Issue:** Critical setting - notebooks should NOT be executed during build
- **Impact:** If not set correctly:
  - Build will try to execute all code cells
  - Build time will be much longer
  - Build might fail if code has dependencies
  - Could overwrite existing outputs in notebooks
- **Search Required:** ✓ HIGH priority
  - Must find equivalent in myst.yml
  - Look for: `project.execute`, `jupyter.execute`, or similar
- **Workaround:** If can't find setting, may need to use CLI flag

#### 7. **Chapter Numbering**
- **Current:** Chapters are numbered via `numbered: True` in _toc.yml
- **Issue:** Unknown how to enable in myst.yml
- **Impact:** Chapters may not show numbers (1., 2., 3., etc.)
  - Cosmetic issue - doesn't break functionality
  - But numbering is important for a textbook
- **Search Required:** ✓ Medium priority
  - Look for: numbering options in project.toc
- **Workaround:** Manually add chapter numbers to titles

#### 8. **Parts/Sections Structure**
- **Current:** TOC has 3 parts: Front Matter, Chapters, End Matter
- **Issue:** Unknown how to create part groupings in myst.yml
- **Impact:** May have flat TOC instead of grouped structure
  - Less organized navigation
  - May confuse readers
- **Search Required:** ✓ Medium priority
  - Look for: nested structure, parts, sections in myst.yml TOC
- **Workaround:** Use flat structure, or investigate after initial build

---

### 🔴 HIGH RISK - Definitely Needs Solution

#### 9. **Custom HTML Footer (CC License)**
- **Current:** Complex HTML footer with Creative Commons license
  ```html
  <div style="text-align: left;">
    <a rel="license" href="https://creativecommons.org/licenses/by-nc-sa/4.0/">
      <img alt="Creative Commons License" ... />
    </a>
    ...
  </div>
  ```
- **Issue:** No known way to add custom HTML in myst.yml
- **Impact:** License information will be missing
  - Legal/attribution issue
  - Need to maintain CC-BY-NC-SA-4.0 license notice
- **Search Required:** ✓ CRITICAL
  - Look for: HTML injection, footer customization, license field
  - May need `project.license` field
  - May need custom template
- **Workaround Options:**
  1. Add license to index.md page
  2. Use `project.license: CC-BY-NC-SA-4.0` field if exists
  3. Create custom template (advanced)
  4. Manually inject HTML after build (hacky)

#### 10. **Repository Button**
- **Current:** `html.use_repository_button: true`
- **Issue:** Unknown if auto-enabled with `project.github` URL
- **Impact:** Readers can't easily find source repository
  - Less convenient but not critical
- **Search Required:** ✓ Medium priority
  - May be automatic with github URL
  - Look for: site.options for button configuration
- **Workaround:** Add repository link to index.md

#### 11. **Build Command Change**
- **Current:** `jb build .`
- **New:** `jupyter book build --html --strict` (from other projects)
- **Issue:** Different command syntax
- **Impact:** build.sh needs updating
- **Solution:** ✅ Known - update build.sh
  ```bash
  # Old
  jb build .
  
  # New
  jupyter book build --html --strict
  # or with BASE_URL for GitHub Pages
  BASE_URL=/ThinkPython/ jupyter book build --html --strict
  ```

---

## Configuration Options to Research

### Priority 1 (Critical)
1. [ ] How to disable notebook execution in myst.yml
2. [ ] How to add CC license footer or license field
3. [ ] How to configure MyST extensions

### Priority 2 (Important)
4. [ ] How to enable chapter numbering
5. [ ] How to create parts/sections in TOC
6. [ ] How to enable repository button
7. [ ] MathJax configuration (if needed)

### Priority 3 (Nice to Have)
8. [ ] Custom logo or favicon
9. [ ] Other theme customizations
10. [ ] PDF/LaTeX export settings

---

## Testing Strategy

### Phase 1: Minimal Viable Config
1. Create jb2/ with basic myst.yml (title, author, github, simple TOC)
2. Copy notebooks without modifications
3. Try to build
4. Document errors and warnings

### Phase 2: Iterative Fixes
5. Fix critical issues (execution, extensions)
6. Add missing configurations based on errors
7. Compare output to JB 1.x version

### Phase 3: Feature Parity
8. Add chapter numbering
9. Add parts/sections structure
10. Add license footer
11. Verify all MyST features work

### Phase 4: Polish
12. Test all links and navigation
13. Verify GitHub button and repository link
14. Check responsive design
15. Final comparison with JB 1.x output

---

## Files to Copy to jb2/

### ✅ Essential Files
- All notebooks: `chap00.ipynb` through `chap19.ipynb`
- `index.md` (landing page)
- `blank.md` (blank notebooks page)
- `prep_notebooks.py` (notebook processor)

### ✅ Build Files (to be modified)
- `build.sh` → update for JB 2.0 commands
- Create new `myst.yml` (not copied, created fresh)
- Consider creating `Makefile` (like other projects)

### ❌ Do NOT Copy
- `_config.yml` (replaced by myst.yml)
- `_toc.yml` (replaced by myst.yml)
- `_build/` directory (generated files)

### ❓ Optional Files
- Support scripts or data files (if any exist)
- Images or assets (if not in notebooks)

---

## Risk Summary

| Issue | Risk Level | Blocker? | Workaround Available? |
|-------|-----------|----------|----------------------|
| prep_notebooks.py | 🟢 Low | No | N/A - should work |
| ghp-import | 🟢 Low | No | Yes - add .nojekyll |
| MyST extensions | 🟡 Medium | Possible | Test defaults first |
| Notebook execution | 🟡 Medium | **Yes** | Must find solution |
| Chapter numbering | 🟡 Medium | No | Manual numbers |
| Parts/sections | 🟡 Medium | No | Flat structure |
| CC License footer | 🔴 High | Maybe | Add to page content |
| Repository button | 🟡 Medium | No | Add manual link |
| Build command | 🟢 Low | No | Known solution |
| MathJax config | 🟡 Medium | No | Use defaults |

**Overall Assessment:** Migration is feasible, but 2-3 critical configurations need to be researched before we can build successfully.

---

## Recommended Next Steps

1. ✅ Complete this issues analysis (done)
2. Complete Task 2.3: Plan file organization
3. Create jb2/ directory with minimal config
4. **Test build immediately** to get real error messages
5. Use error messages to guide configuration research
6. Iterate until build succeeds
7. Compare output and fix remaining issues

The "test early" approach is better than trying to perfect the config upfront, since build errors will tell us exactly what's needed.

