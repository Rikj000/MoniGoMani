# Contributing to MGM

👍🎉 First off, thanks for taking the time to contribute! 🎉👍

The following is a set of guidelines for contributing to the MoniGoMani Hyper Strategy and its modules, which are hosted in the [Rikj000](https://github.com/Rikj000/MoniGoMani) repository on GitHub. These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

## Local development

### Git Commit Hook(s)

This project uses a set of git commit hooks to help us developers to write – *and more important, commit & push* – code mostly in the same fashion. These hooks are configured in `.pre-commit-config.yaml` and can be run on your dev machine by using an automated `pre-commit` integration.

See [Pre-commit](https://pre-commit.com) for usage and installation instructions.

### GitHub Action Workflows

GitHub Actions are used in order to run automated unit-tests against our code. These actions are triggered at push-events into main, development and feature/* branches. These actions are also triggered at every Pull Request so we all can see very quickly if something happened.

It can be quite handy to run a GitHub action workflow on your local machine. And then `act` is your friend.

[Go to `act` website](https://github.com/nektos/act)

<hr>

*Note; this document is inspired by the awesome Atom contributing guidelines https://github.com/atom/atom/blob/master/CONTRIBUTING.md*

<hr>
