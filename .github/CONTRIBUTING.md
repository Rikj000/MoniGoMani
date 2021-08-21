# Contributing to MoniGoMani Hyper Strategy

👍🎉 First off, thanks for taking the time to contribute! 🎉👍


The following is a set of guidelines for contributing to the MoniGoMani Hyper Strategy and its modules, which are hosted in the [Rikj000 repository](https://github.com/Rikj000/MoniGoMani) on GitHub. These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

---

Table of Contents
-

- [Contributing to MoniGoMani Hyper Strategy](#contributing-to-monigomani-hyper-strategy)
  - [Installation instructions](#installation-instructions)
  - [Using pre-commit hooks](#using-pre-commit-hooks)
  - [GitHub Action Workflows](#github-action-workflows)

---

Installation instructions
------

We use `pipenv` for virtual environments. We install all packages and its dependencies using `pipenv`. Also we run all commands using `pipenv` to ensure we've the right dependencies and do not interfere with other environments or dependencies.

**To Install `pipenv` and the required packages**:
```bash
pip install pipenv

pipenv install --dev
```

**Try, and run for example all unit tests**:

```bash
pipenv run pytest -c pytest.ini tests/
```

Using pre-commit hooks
------

This project uses a set of git commit hooks to help us developers to write – *and more important, maintain* – code mostly in the same style & fashion. These hooks are configured in `.pre-commit-config.yaml` and can be run on your machine by using an automated [pre-commit](https://pre-commit.com) integration.

**Run pre-commit only at changed files:**

```bash
pipenv run pre-commit run --from-ref HEAD^^^ --to-ref HEAD
```

**Run pre-commit at all files:**

```bash
$ pipenv run pre-commit run --all

~/Projects/MoniGoMani(master) » pre-commit run --all

Trim Trailing Whitespace.................................................Passed
Fix End of Files.........................................................Passed
Check python ast.........................................................Passed
Check docstring is first.................................................Passed
Check JSON...............................................................Passed
Check for added large files..............................................Passed
Check Yaml...............................................................Passed
Debug Statements (Python)................................................Passed
Tests should end in _test.py.............................................Passed
Fix double quoted strings................................................Failed
- hook id: double-quote-string-fixer
- exit code: 1
- files were modified by this hook

Fixing strings in mgm-hurry

Fix requirements-mgm.txt.................................................Passed
Check for case conflicts.................................................Passed
```

See https://pre-commit.com for usage and installation instructions.

GitHub Action Workflows
------

GitHub Actions are used in order to run automated unit-tests against our code. These actions are triggered at push-events into main, development and feature/* branches. These actions are also triggered at every Pull Request so we all can see very quickly if something happened.

It can be quite handy to run a GitHub action workflow on your local machine. Well, [act](https://github.com/nektos/act) is your friend.

---

![mgm tests](https://github.com/topscoder/MoniGoMani/workflows/pytest-unit-tests/badge.svg)
![mgm style guide](https://github.com/topscoder/MoniGoMani/actions/workflows/flake8.yml/badge.svg)