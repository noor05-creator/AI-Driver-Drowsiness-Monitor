# Contributing to Driver Drowsiness Monitor

Thank you for being part of this project. This document defines the exact rules every team member must follow to keep the codebase clean, conflict-free, and submission-ready.

Read this fully before writing a single line of code.

---

## Table of Contents

1. [Branching Rules](#branching-rules)
2. [Commit Message Format](#commit-message-format)
3. [Pull Request Process](#pull-request-process)
4. [Pull Request Template](#pull-request-template)
5. [Code Style Rules](#code-style-rules)
6. [Flake8 Error Codes — What They Mean and How to Fix Them](#flake8-error-codes--what-they-mean-and-how-to-fix-them)
7. [Docstring Requirements](#docstring-requirements)
8. [What NOT to Commit](#what-not-to-commit)
9. [Reviewer Responsibilities](#reviewer-responsibilities)

---

## 1. Branching Rules

### Branch structure
```
main          ← stable, submission-ready. Never commit directly here.
dev           ← integration branch. All feature branches merge into dev first.
feature/<name> ← your working branch for each issue.
fix/<name>     ← for bug fix issues only.
docs/<name>    ← for documentation-only issues.
```

### Rules

- **Never push directly to `main` or `dev`.** All changes go through a Pull Request.
- One branch per issue. Do not combine multiple issues on one branch.
- Branch names must be lowercase with hyphens, no spaces.
- Always branch off from `dev`, not `main`.

### Creating your branch correctly

```bash
# Step 1: Switch to dev and pull latest changes
git checkout dev
git pull origin dev

# Step 2: Create your feature branch
git checkout -b feature/eye-detection

# Step 3: Work and commit on your branch
# Step 4: Push your branch
git push origin feature/eye-detection

# Step 5: Open a Pull Request from your branch → dev
```

### Branch naming examples

| Issue | Correct branch name |
|---|---|
| #5 Face & eye detection | `feature/eye-detection` |
| #6 Train CNN | `feature/cnn-training` |
| #8 Main pipeline | `feature/main-pipeline` |
| #12 Pygame game | `feature/reaction-game` |
| #14 Webcam error handling | `fix/webcam-errors` |
| #15 Docstrings | `docs/docstrings` |

---

## 2. Commit Message Format

Every commit message must follow this format exactly:
```
<type>: <short description in lowercase>
```
### Types

| Type | When to use |
|---|---|
| `feat` | Adding new functionality |
| `fix` | Fixing a bug |
| `docs` | README, comments, docstrings only |
| `refactor` | Restructuring code without changing behavior |
| `test` | Adding or updating tests |
| `chore` | Dependencies, config files, .gitignore |

### Rules

- Description must be lowercase
- No period at the end
- Keep it under 72 characters
- Use present tense — "add feature" not "added feature"

### Good examples
```
feat: implement eye aspect ratio calculation
feat: add CNN training script with 20 epochs
fix: prevent alarm from stacking on every frame
fix: handle missing webcam gracefully
docs: add docstrings to detector.py functions
refactor: extract eye ROI logic into separate function
chore: add opencv and dlib to requirements.txt
```

### Bad examples
```
### Bad examples
updated stuff                  ← no type, too vague
Fixed Bug.                     ← capitalized, has period
feat: Added the EAR Function   ← past tense, capitalized
wip                            ← meaningless
```
### Automated Commit Message Enforcement

Every commit message is automatically validated when you open a PR.
If any commit in your branch fails the format check, the PR will be
blocked with a red check showing exactly which commit failed and why.

Rules enforced automatically:
- Type must be one of: feat, fix, docs, refactor, test, chore
- Type must be lowercase
- Description must be lowercase
- Description cannot be empty
- No period at the end of the message
- Maximum 72 characters total

Fix a bad commit message using:
```bash
# If it is your most recent commit
git commit --amend -m "feat: correct message here"
git push --force origin your-branch-name

# If it is an older commit you need to fix
git rebase -i HEAD~3
# Change 'pick' to 'reword' on the commit you want to fix
# Save and enter the new message when prompted
git push --force origin your-branch-name
```

Never use --force on main or dev. Only on your own feature branches.
---

## 3. Pull Request Process

### Step-by-step

1. Finish your work on your `feature/` branch
2. Make sure your code runs without errors
3. Pull latest `dev` and resolve any conflicts on your branch before opening the PR
4. Open a Pull Request from your branch into `dev`
5. Fill in the PR template below completely — do not leave any section blank
6. Request review from at least one other team member
7. Do not merge your own PR — the reviewer merges it after approval
8. Delete your branch after it is merged

### Before opening a PR, verify

- [ ] Code runs without errors (`python <yourfile>.py`)
- [ ] No debug `print()` statements left in the code
- [ ] All functions have docstrings
- [ ] Inline comments added to complex logic
- [ ] No large files committed (no `.h5`, `.dat`, images, `venv/`)
- [ ] `.gitignore` entries respected
- [ ] Branch is up to date with `dev`

---

## 4. Pull Request Template

Create a file at `.github/PULL_REQUEST_TEMPLATE.md` and paste the following. GitHub will auto-load this template every time a PR is opened.

```markdown
## Summary
<!-- One or two sentences describing what this PR does -->

## Related Issue
Closes #<issue number>

## Type of Change
<!-- Put an x in the box that applies -->
- [ ] feat — new feature
- [ ] fix — bug fix
- [ ] docs — documentation only
- [ ] refactor — code restructure, no behavior change
- [ ] chore — config, dependencies

## What was implemented
<!-- Bullet list of exactly what you built -->
-
-
-

## How to test
<!-- Step by step instructions for the reviewer to verify your work -->
1.
2.
3.

## Screenshots / Output
<!-- Paste a screenshot, terminal output, or chart if applicable -->

## Checklist
- [ ] Code runs without errors
- [ ] No debug print statements
- [ ] All functions have docstrings
- [ ] No model files, dataset images, or venv committed
- [ ] Branch is up to date with dev
- [ ] Requested review from a team member
```

---

## 5. Code Style Rules

- Use 4 spaces for indentation — never tabs
- Maximum line length: 79 characters (PEP8 standard)
- One blank line between logical blocks inside a function
- Two blank lines between top-level functions and classes
- All variable names: `snake_case`
- All constants: `UPPER_SNAKE_CASE`
- No unused imports — remove them before committing
- No hardcoded file paths — use `os.path.join()` for all paths

---

### Flake8 Error Codes — What They Mean and How to Fix Them

When your PR fails the automated style check, click "Details" on the
failed check. You will see output like this:
    ./detector.py:12:80: E501 line too long (95 > 79 characters)
    ./main.py:3:1: F401 'os' imported but unused
Format is always:
    filename : line number : column number : error code : description

    Go to the exact file and line number shown and apply the fix below:

| Code | Problem | Fix |
|---|---|---|
| `E501` | Line longer than 79 characters | Break into multiple shorter lines |
| `E302` | Missing 2 blank lines before a function | Add 2 blank lines before `def` |
| `E303` | Too many blank lines | Remove extra blank lines |
| `E111` | Indentation is not a multiple of 4 spaces | Use 4 spaces, never tabs |
| `E117` | Over-indented code | Reduce indentation level |
| `W291` | Trailing whitespace at end of line | Remove invisible spaces at line end |
| `W293` | Whitespace on a blank line | Clear blank lines completely |
| `W292` | No newline at end of file | Add one blank line at end of file |
| `F401` | Imported but unused | Delete the unused import |
| `F821` | Undefined variable name | Check spelling or missing import |
| `E711` | Comparison to None using == | Change `== None` to `is None` |
| `E712` | Comparison to True/False using == | Change `== True` to `is True` |
| `W503` | Line break before binary operator | Move operator to end of previous line |
| `E231` | Missing whitespace after comma or colon | Add a space after `,` `:` |
| `E225` | Missing whitespace around operator | Add spaces around `=` `+` `-` etc |

### How to check your code BEFORE pushing

Run flake8 locally on your branch before opening a PR so you catch
errors yourself first:

```bash
# Install flake8 if you haven't already
pip install flake8

# Check a specific file
flake8 detector.py --max-line-length=79

# Check all files at once
flake8 . --max-line-length=79 --exclude=venv,__pycache__
```

Fix every error it reports, then push. The PR check should pass green.

### Important

Flake8 checks code style only — not whether your logic is correct.
Passing the style check does not mean your code works. You are still
responsible for testing your own code before opening a PR.


## 6. Docstring Requirements

Every function must have a docstring in this format:

```python
def eye_aspect_ratio(eye):
    """
    Calculate the Eye Aspect Ratio (EAR) for a given eye.

    EAR is used to detect blink and eye closure states.
    A value below 0.25 typically indicates a closed eye.

    Args:
        eye (numpy.ndarray): Array of 6 (x, y) landmark coordinates
                             representing the eye contour points.

    Returns:
        float: The Eye Aspect Ratio value. Lower values indicate
               more closed eyes.
    """
```

---

## 7. What NOT to Commit

These must always be in `.gitignore` and must never appear in any commit:

| File / Folder | Reason |
|---|---|
| `venv/` | Virtual environment — everyone creates their own |
| `*.h5` | Trained model — too large, share via Google Drive |
| `shape_predictor_68_face_landmarks.dat` | 95MB dlib file |
| `data/open/`, `data/closed/` | Dataset images — share via Google Drive |
| `logs/*.csv` | Session logs — machine-specific |
| `assets/*.png` | Generated charts — recreated by running scripts |
| `__pycache__/` | Python bytecode |
| `.DS_Store` | macOS system file |
| `*.pyc` | Compiled Python files |

If you accidentally commit any of these, tell the team lead immediately.

---

## 8. Reviewer Responsibilities

When you are assigned as a reviewer on a Pull Request:

- Review within 24 hours of being assigned
- Check that the PR template is filled in completely
- Pull the branch and run the code yourself to verify it works
- Check that all functions have docstrings
- Check that no forbidden files are included
- Leave specific comments on lines that need changes — do not just write "fix this"
- Approve only when all checklist items pass
- You merge the PR after approving — the author does not merge their own

---

## Questions

If you are unsure about anything, open a GitHub Discussion or message the team lead before starting work. Do not guess and commit broken code.