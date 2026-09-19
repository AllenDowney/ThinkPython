# Task 2.3: File Organization Plan for jb2/

> **Note:** This is reference material for a **deferred migration project** (as of Jan 12, 2026).  
> JB 2.0 migration is on hold. The jb2/ directory was never created.  
> Keep this file for future reference if/when migration becomes necessary.

---

## Directory Structure

```
/home/downey/ThinkPython/
├── jb/                          # Existing JB 1.x (keep unchanged)
│   ├── _config.yml
│   ├── _toc.yml
│   ├── build.sh
│   ├── *.ipynb
│   └── ...
│
└── jb2/                         # New JB 2.0 (to be created)
    ├── myst.yml                 # NEW - main configuration
    ├── Makefile                 # NEW - build automation
    ├── build.sh                 # MODIFIED - updated for JB 2.0
    ├── prep_notebooks.py        # COPIED - no changes expected
    ├── index.md                 # COPIED
    ├── blank.md                 # COPIED
    ├── chap00.ipynb             # COPIED
    ├── chap01.ipynb             # COPIED
    ├── chap02.ipynb             # COPIED
    ├── ... (all chapters)
    └── chap19.ipynb             # COPIED
```

---

## Files to Create (New)

### 1. myst.yml
**Source:** Create from scratch based on config_mapping.md
**Purpose:** Main configuration replacing _config.yml + _toc.yml
**Initial Version:** Use proposed config from config_mapping.md

### 2. Makefile (Optional but Recommended)
**Source:** Based on BayesFertility and HALE examples
**Purpose:** Standardize build commands
**Template:**
```makefile
.PHONY: help build build-local clean deploy serve

help:
	@echo "Available commands:"
	@echo "  make build       - Build for GitHub Pages"
	@echo "  make build-local - Build for local preview"
	@echo "  make clean       - Clean build artifacts"
	@echo "  make deploy      - Build and deploy to GitHub Pages"
	@echo "  make serve       - Build and serve locally"

build:
	BASE_URL=/ThinkPython/ jupyter book build --html --strict
	touch _build/html/.nojekyll

build-local:
	jupyter book build --html --strict

clean:
	rm -rf _build

deploy: build
	ghp-import -n -p -f _build/html

serve: build-local
	cd _build/html && python -m http.server 8000
```

---

## Files to Copy (From jb/ to jb2/)

### Content Files (Copy As-Is)

#### Markdown Files
- ✅ `index.md` - Landing page with book introduction
- ✅ `blank.md` - Blank notebooks page

#### Notebook Files  
- ✅ `chap00.ipynb` - Preface
- ✅ `chap01.ipynb` through `chap19.ipynb` - All 19 chapters

**Copy Command:**
```bash
cp jb/index.md jb2/
cp jb/blank.md jb2/
cp jb/chap*.ipynb jb2/
```

### Script Files (Copy and Potentially Modify)

#### prep_notebooks.py
- ✅ Copy as-is initially
- ✅ Test after copying
- 🔍 Modify only if issues arise

**Copy Command:**
```bash
cp jb/prep_notebooks.py jb2/
```

#### build.sh (Copy and Modify)
**Action:** Copy then update commands for JB 2.0

**Current (JB 1.x):**
```bash
# copy the notebooks
cp ../ThinkPythonSolutions/soln/chap[01][0-9]*.ipynb .

# add tags to hide the solutions
python prep_notebooks.py

# build the HTML version
jb build .

# push it to GitHub
ghp-import -n -p -f _build/html
```

**Updated (JB 2.0):**
```bash
#!/bin/bash
# Build script for Think Python - Jupyter Book 2.0

# Copy the notebooks from solutions directory
cp ../ThinkPythonSolutions/soln/chap[01][0-9]*.ipynb .

# Process notebooks (remove solutions, add labels)
python prep_notebooks.py

# Build the HTML version with JB 2.0
BASE_URL=/ThinkPython/ jupyter book build --html --strict

# Create .nojekyll file for GitHub Pages
touch _build/html/.nojekyll

# Push to GitHub Pages
ghp-import -n -p -f _build/html
```

---

## Files NOT to Copy

### Configuration Files
- ❌ `_config.yml` - Replaced by myst.yml
- ❌ `_toc.yml` - Integrated into myst.yml

### Build Artifacts
- ❌ `_build/` - Generated directory, will be created fresh
- ❌ `__pycache__/` - Python cache, will be regenerated

---

## File Modification Summary

| File | Action | Priority | Complexity |
|------|--------|----------|------------|
| myst.yml | CREATE | 🔴 Critical | Medium |
| Makefile | CREATE | 🟡 Optional | Low |
| build.sh | COPY & MODIFY | 🟢 Important | Low |
| prep_notebooks.py | COPY | 🟢 Important | None |
| index.md | COPY | 🟢 Required | None |
| blank.md | COPY | 🟢 Required | None |
| chap*.ipynb | COPY | 🟢 Required | None |

---

## Implementation Steps

### Step 1: Create Directory Structure
```bash
cd /home/downey/ThinkPython
mkdir jb2
cd jb2
```

### Step 2: Copy Content Files
```bash
# From /home/downey/ThinkPython/jb2/
cp ../jb/index.md .
cp ../jb/blank.md .
cp ../jb/chap*.ipynb .
cp ../jb/prep_notebooks.py .
```

### Step 3: Create New Configuration Files
1. Create `myst.yml` from template in config_mapping.md
2. Create `Makefile` from template above
3. Copy and modify `build.sh`

### Step 4: Verify File Structure
```bash
ls -la
# Should see:
# - myst.yml
# - Makefile (optional)
# - build.sh
# - prep_notebooks.py
# - index.md
# - blank.md
# - chap00.ipynb through chap19.ipynb
```

---

## Testing Checklist After Setup

- [ ] All 20 notebooks copied (chap00-19)
- [ ] index.md and blank.md present
- [ ] prep_notebooks.py present and executable
- [ ] myst.yml created with valid YAML syntax
- [ ] build.sh updated and executable
- [ ] Makefile created (if using)
- [ ] No _config.yml or _toc.yml in jb2/
- [ ] No _build/ directory yet

---

## File Count Verification

**Expected files in jb2/ after initial setup:**
- 20 notebooks (chap00.ipynb through chap19.ipynb)
- 2 markdown files (index.md, blank.md)
- 1 Python script (prep_notebooks.py)
- 1 config file (myst.yml)
- 1-2 build files (build.sh, and optionally Makefile)

**Total: 24-25 files**

---

## Safety Considerations

### Keep JB 1.x Intact
- 🔒 Do NOT modify anything in `jb/` directory
- 🔒 Keep as reference and fallback
- 🔒 Can compare outputs side-by-side

### Version Control
- ✅ Commit jb2/ setup before first build
- ✅ Create git branch for JB 2.0 migration
- ✅ Easy to revert if needed

### Backup Strategy
- 🔄 Original jb/ remains unchanged
- 🔄 Can always regenerate jb2/ from scratch
- 🔄 Build artifacts are in _build/ (gitignored)

---

## Next Steps After File Organization

1. ✅ Create jb2/ directory
2. ✅ Copy all necessary files
3. ✅ Create myst.yml
4. ✅ Create/modify build files
5. 🔍 **Test build** - `make build-local` or `jupyter book build --html --strict`
6. 📝 Document errors and iterate
7. 🔧 Fix configuration issues
8. ✨ Compare output with jb/ version

---

## Decision Points

### Use Makefile or build.sh?
**Recommendation:** Create both
- Makefile for developer convenience (make build, make serve, etc.)
- build.sh for compatibility with existing workflow
- Makefile can call build.sh or duplicate commands

### Modify prep_notebooks.py now or later?
**Recommendation:** Copy as-is, modify only if needed
- Likely works unchanged
- Test first, fix only if broken
- Document any changes needed

### Create full myst.yml or minimal?
**Recommendation:** Start minimal, iterate
- Basic: title, author, github, simple TOC
- Test build to see what errors occur
- Add configurations based on real needs
- Easier to debug with minimal config

---

## Status: Ready for Implementation

All planning complete. Clear file structure defined. Ready to proceed to Phase 3: Implementation.

