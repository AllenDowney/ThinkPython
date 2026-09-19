# Jupyter Book 2.0 Upgrade Plan

## Project: Think Python

**Date Created:** January 12, 2026  
**Status:** ⏸️ **ON HOLD / DEFERRED**

---

## Executive Summary

**Decision:** After thorough research and planning, the migration to Jupyter Book 2.0 is **deferred indefinitely**.

**Reason:** Too many critical unknowns (notebook execution settings, CC license footer, MyST extensions configuration) combined with a perfectly functioning JB 1.x setup. No compelling reason to risk breaking a working system.

**Outcome:** Continue using Jupyter Book 1.x. Revisit migration only if JB 1.x becomes problematic or JB 2.0 becomes necessary.

**Value:** All planning work (config mapping, issues analysis, file organization) is preserved for future use if/when migration becomes necessary.

---

## Phase 1: Research and Review

### Task 1.1: Review Existing Configuration
- [x] Review current JB configuration in `/home/downey/ThinkPython/jb`
  - Current config uses JB 1.x format (_config.yml + _toc.yml)
  - Book settings: title, author, latex, execute, repository, html customization
  - MyST extensions enabled: amsmath, colon_fence, deflist, dollarmath, fieldlist, html_admonition, html_image, linkify, replacements, smartquotes, strikethrough, substitution, tasklist
  - Custom MathJax configuration
  - Creative Commons license footer
  - execute_notebooks: 'off'
  - Structure: 19 chapters + index + blank notebooks page

### Task 1.2: Review Configurations from Other Projects
- [x] Review `/home/downey/BayesFertility/jb` configuration
  - Uses JB 2.0 with myst.yml
  - Structure: version 1, project section with title/github/toc, site section with template/title/options
  - Simple 3-file TOC: index, blog_post, tech_report
  - Build command: `jupyter book build --html --strict` (NOT myst CLI)
  - Deployment: ghp-import with BASE_URL for GitHub Pages
- [x] Review `/home/downey/EqualityWEF/HALE/jb` configuration
  - Uses JB 2.0 with myst.yml
  - Similar structure with project ID
  - Larger TOC: 10 pages including index, summary, tech reports, etc.
  - Same build/deploy approach as BayesFertility
- [x] Document common patterns and best practices from these projects
  - Both use `jupyter book build` command (not MyST CLI)
  - Both use book-theme template
  - Both use Makefile for build automation
  - Both use ghp-import for GitHub Pages deployment
  - Both use BASE_URL for GitHub project pages
- [x] Identify any features/patterns that should be adopted for ThinkPython
  - Makefile approach for build automation
  - BASE_URL configuration for GitHub Pages
  - Clean separation between build-local and deploy builds

### Task 1.3: Research Jupyter Book 2.0
- [x] Review JB 2.0 documentation and migration guide
  - Key insight: Can still use `jupyter book build` command with myst.yml
  - No need to switch to MyST CLI for basic usage
- [x] Understand myst.yml structure and syntax
  - Top level: version (1), project, site sections
  - project: title, github, toc (list of files with optional title overrides)
  - site: template (book-theme), title, options (logo_text, etc.)
- [x] Identify breaking changes from JB 1.x to 2.0
  - Single myst.yml replaces _config.yml + _toc.yml
  - Different TOC syntax (list of files under project.toc)
  - Need to research: MyST extensions, execution settings, Sphinx config
- [ ] Document new features available in JB 2.0
  - Need to research what's new/improved
- [x] Research MyST Markdown CLI vs jupyter-book CLI
  - jupyter-book CLI still works with myst.yml (verified from other projects)
  - This simplifies migration - no need to switch CLI tools

---

## Phase 2: Migration Planning

### Task 2.1: Map Current Configuration to JB 2.0 ✅
- [x] Map _config.yml settings to myst.yml format
  - ✅ Project metadata (title, author, license) → project section
  - ✅ Repository settings → project.github
  - ❓ HTML options (footer, buttons) → site.options (need to research)
  - ❓ MyST parser extensions → unknown (need to research/test)
  - ❓ Sphinx/MathJax configuration → unknown (need to research/test)
  - ❓ Execution settings → unknown (need to research/test)
- [x] Map _toc.yml structure to myst.yml format
  - ✅ Root document → first entry in project.toc
  - ❓ Parts/sections structure → unknown how to group in JB 2.0
  - ❓ Chapter numbering → unknown how to enable
  - ✅ File references → simple list format
- [x] Created detailed config_mapping.md document with proposed myst.yml

### Task 2.2: Identify Potential Issues ✅
- [x] Check compatibility of current MyST extensions with JB 2.0
  - 🟡 13 extensions to configure - unknown how in myst.yml
- [x] Verify MathJax configuration compatibility
  - 🟡 Custom MathJax config - unknown how in myst.yml (low priority - minimal math usage)
- [x] Verify custom HTML footer and CC license formatting
  - 🔴 HIGH RISK - no known way to add custom HTML footer
  - Need to research: license field, footer options, or workarounds
- [x] Check if prep_notebooks.py workflow needs changes
  - 🟢 LOW RISK - should work unchanged (manipulates notebook JSON)
- [x] Review build.sh script for necessary updates
  - 🟢 Known changes: `jb build .` → `jupyter book build --html --strict`
  - Add: `touch _build/html/.nojekyll`
- [x] Check ghp-import deployment process compatibility
  - 🟢 LOW RISK - same command works (verified from other projects)
- [x] **Critical Finding:** Must find how to disable notebook execution
  - Currently: `execute_notebooks: 'off'` - MUST have equivalent in myst.yml
- [x] Created detailed issues_analysis.md with risk assessment and testing strategy

### Task 2.3: Plan File Organization ✅
- [x] Decide which files to copy to jb2/
  - ✅ Content files: chap00-19.ipynb (20 notebooks), index.md, blank.md
  - ✅ Build scripts: build.sh (modify), prep_notebooks.py (copy as-is)
  - ✅ New files: myst.yml (create), Makefile (optional, create)
- [x] Plan directory structure for jb2/
  - ✅ Parallel to jb/, same content files, new config format
  - ✅ Keep jb/ unchanged as reference/fallback
- [x] Determine if any files should NOT be copied
  - ❌ Don't copy: _config.yml, _toc.yml, _build/, __pycache__/
- [x] Created detailed file_organization_plan.md with:
  - File-by-file copy plan
  - Modified build.sh template
  - Makefile template (from other projects)
  - Implementation steps and verification checklist

---

## Phase 3: Implementation

### Task 3.1: Create jb2 Directory Structure
- [ ] Create `/home/downey/ThinkPython/jb2` directory
- [ ] Copy content files from jb/ to jb2/
  - All chapter notebooks (chap00-chap19.ipynb)
  - index.md
  - blank.md
  - prep_notebooks.py
- [ ] Copy/adapt build.sh script
- [ ] Do NOT copy _build/ directory

### Task 3.2: Create myst.yml Configuration
- [ ] Create new myst.yml file in jb2/
- [ ] Configure project metadata
- [ ] Configure site settings
- [ ] Configure table of contents
- [ ] Configure MyST extensions
- [ ] Configure execution settings
- [ ] Configure HTML/theme settings
- [ ] Add repository and GitHub Pages settings
- [ ] Add Creative Commons license

### Task 3.3: Update Build Process
- [ ] Update build.sh for JB 2.0 commands
- [ ] Test prep_notebooks.py compatibility
- [ ] Verify ghp-import still works with new build output

---

## Phase 4: Testing

### Task 4.1: Initial Build Test
- [ ] Run initial build with JB 2.0
- [ ] Review build output and warnings
- [ ] Fix any immediate errors

### Task 4.2: Content Verification
- [ ] Verify all chapters render correctly
- [ ] Check MathJax/LaTeX rendering
- [ ] Verify code cells display properly
- [ ] Check notebook execution settings (should be 'off')
- [ ] Verify index page and navigation
- [ ] Check blank notebooks page

### Task 4.3: Feature Testing
- [ ] Test repository button functionality
- [ ] Verify Creative Commons footer displays
- [ ] Check MyST extensions work (math, admonitions, etc.)
- [ ] Test responsive design / mobile view
- [ ] Verify search functionality
- [ ] Test any interactive elements

### Task 4.4: Comparison Testing
- [ ] Compare JB 1.x output vs JB 2.0 output
- [ ] Document differences (visual, functional)
- [ ] Ensure no regressions
- [ ] Identify improvements

---

## Phase 5: Documentation and Finalization

### Task 5.1: Document Changes
- [ ] Create MIGRATION.md documenting the upgrade process
- [ ] Document any breaking changes or gotchas
- [ ] Update README if needed
- [ ] Document new build commands

### Task 5.2: Review and Decision
- [ ] Final review of JB 2.0 version
- [ ] Compare pros/cons vs JB 1.x
- [ ] Decide whether to proceed with migration
- [ ] Plan deprecation of jb/ directory if migrating

### Task 5.3: Deployment Planning
- [ ] Test GitHub Pages deployment
- [ ] Plan cutover strategy
- [ ] Consider maintaining both versions temporarily
- [ ] Update any external links if needed

---

## Key Findings from JB 2.0 Projects

### BayesFertility myst.yml Structure
```yaml
version: 1
project:
  title: Bayesian Fertility Rate Projections
  github: https://github.com/AllenDowney/BayesFertility
  toc:
    - file: index.md
    - file: blog_post.md
      title: Blog Post
    - file: tech_report.md
      title: Technical Report
site:
  template: book-theme
  title: Bayesian Fertility Rate Projections
  options:
    logo_text: Bayesian Fertility Rate Projections
```

### HALE/EqualityWEF myst.yml Structure
- Includes optional `project.id` field
- More extensive TOC (10 pages)
- Same site/template configuration

### Build Process from Both Projects
- Command: `jupyter book build --html --strict`
- For GitHub Pages: `BASE_URL=/ProjectName/ jupyter book build --html --strict`
- Creates `.nojekyll` file in `_build/html/`
- Uses ghp-import for deployment: `ghp-import -n -p -f _build/html`
- Makefile provides: build, build-local, clean, deploy, serve targets

### Questions Still to Address
1. How to configure MyST extensions in myst.yml format?
2. How to configure execution settings (execute_notebooks: 'off')?
3. How to add custom HTML footer with CC license?
4. How to configure MathJax settings?
5. How to configure repository button?
6. How to handle sphinx-specific configurations?

---

## Notes

### Current JB 1.x Configuration Highlights
- **Title:** Think Python
- **Author:** Allen B. Downey
- **Repository:** https://github.com/AllenDowney/ThinkPython/tree/v3
- **License:** CC BY-NC-SA 4.0
- **Structure:** 
  - Front Matter: chap00
  - Numbered Chapters: chap01-chap19
  - End Matter: blank (blank notebooks page)
- **Build Process:** Copy notebooks from ThinkPythonSolutions, prep them, build, deploy with ghp-import

### Questions to Address
1. Does JB 2.0 support all the current MyST extensions?
2. How does MathJax configuration work in JB 2.0?
3. Can we maintain the same custom footer with CC license?
4. Does the current prep_notebooks.py script need modification?
5. Are there performance improvements in JB 2.0?
6. What new features in JB 2.0 would benefit this book?
7. Is there better support for Colab links in JB 2.0?

### Resources Needed
- Jupyter Book 2.0 documentation
- MyST CLI documentation
- Migration guide from JB 1.x to 2.0
- Access to BayesFertility and EqualityWEF projects for reference

---

## Status: PROJECT ON HOLD ⏸️

### Decision: January 12, 2026
**Migration to JB 2.0 is DEFERRED - Current JB 1.x will remain in use**

### Reason for Decision
After completing thorough planning and research (Phases 1 & 2), we identified too many unknowns and potential issues that would need to be resolved:

**Critical Unknowns:**
- 🔴 How to disable notebook execution in myst.yml (CRITICAL - must not execute notebooks during build)
- 🔴 How to add custom HTML footer for CC-BY-NC-SA-4.0 license (CRITICAL - legal requirement)
- 🟡 How to configure 13 MyST extensions in myst.yml
- 🟡 How to enable chapter numbering
- 🟡 How to create parts/sections structure in TOC
- 🟡 MathJax custom configuration

**Current Situation:**
- ✅ Jupyter Book 1.x is working perfectly
- ✅ Build and deployment pipeline is stable
- ✅ All features are functioning as expected
- ✅ No urgent need to migrate

**Decision:** Don't look for trouble. Keep using JB 1.x until:
1. JB 2.0 documentation becomes more comprehensive
2. There's a compelling feature/requirement that necessitates upgrade
3. JB 1.x becomes unsupported or problematic
4. Community has established clearer migration patterns

---

## Work Completed (Phases 1-2)

### ✓ **Phase 1: Research and Review**
- ✓ Reviewed current JB 1.x configuration
- ✓ Reviewed BayesFertility and HALE JB 2.0 configurations
- ✓ Documented basic myst.yml structure and build process
  
### ✓ **Phase 2: Migration Planning**
- ✓ Task 2.1: Configuration Mapping
  - Created config_mapping.md with detailed translation guide
  - Mapped basic settings, identified unknowns
  - Drafted initial myst.yml structure
- ✓ Task 2.2: Identify Potential Issues
  - Created issues_analysis.md with risk assessment
  - Categorized issues: 🟢 Low / 🟡 Medium / 🔴 High risk
  - Identified critical unknowns
- ✓ Task 2.3: Plan File Organization  
  - Created file_organization_plan.md
  - Defined what to copy, create, and modify
  - Created build.sh and Makefile templates

**Value of Planning Work:**
- All planning documents are preserved for future use
- When/if migration becomes necessary, we have a clear roadmap
- Issues are documented so we know what to research
- Time investment will pay off later

---

## Phases 3-5: NOT STARTED (Deferred)

### Phase 3: Implementation (DEFERRED)
- [ ] Task 3.1: Create jb2 directory structure
- [ ] Task 3.2: Create myst.yml configuration
- [ ] Task 3.3: Update build process

### Phase 4: Testing (DEFERRED)
- [ ] Task 4.1-4.4: Build and content verification

### Phase 5: Documentation and Finalization (DEFERRED)
- [ ] Task 5.1-5.3: Documentation and deployment

---

## Future Migration Triggers

Consider resuming JB 2.0 migration if any of these occur:

1. **Forced Migration:** JB 1.x becomes deprecated or stops working
2. **Feature Need:** A compelling JB 2.0 feature becomes essential
3. **Community Maturity:** Migration patterns become well-documented
4. **Documentation Improvement:** Official docs cover all our critical unknowns
5. **External Requirement:** Publisher, platform, or users require JB 2.0
6. **Breaking Changes:** Current build pipeline breaks and easier to migrate than fix

---

## Resources for Future Reference

### Planning Documents Created
1. `plan.md` - This file, overall project plan
2. `config_mapping.md` - JB 1.x → JB 2.0 configuration mapping
3. `issues_analysis.md` - Risk assessment and potential issues
4. `file_organization_plan.md` - File structure and organization plan

### External References
- Current JB 1.x config: `/home/downey/ThinkPython/jb/_config.yml` and `_toc.yml`
- Working JB 2.0 examples: 
  - `/home/downey/BayesFertility/jb/myst.yml`
  - `/home/downey/EqualityWEF/HALE/jb/myst.yml`

### Key Research Questions (for future)
When resuming, prioritize finding answers to:
1. How to set `execute_notebooks: false` in myst.yml?
2. How to add custom HTML footer in myst.yml?
3. How to configure MyST extensions in myst.yml?
4. How to enable chapter numbering in myst.yml?
5. How to create parts/sections structure in myst.yml TOC?

---

## Current Action: Continue with JB 1.x

**No changes needed** - Keep using existing workflow:
```bash
cd /home/downey/ThinkPython/jb
bash build.sh
```

Everything continues to work as before. JB 2.0 migration can be reconsidered in the future when conditions are more favorable.

