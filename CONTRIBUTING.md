# Contributing to plex-renamer

Thanks for your interest in contributing! This project is modular and designed to grow over time. Contributions of all kinds are welcome — code, documentation, patterns, bug reports, and feature ideas.

## Getting Started

1. Fork the repository on GitHub.
2. Clone your fork locally:
git clone https://github.com/YOURUSER/plex-renamer.git (github.com in Bing)

Code
3. Create a virtual environment:
python -m venv .venv
.\.venv\Scripts\activate

Code
4. Install in editable mode:
pip install -e .

Code

## Making Changes

- Keep modules small and focused.
- Follow the existing package structure:
src/plex_renamer/

Code
- Add tests for new features when possible.
- Update documentation (README, config examples) when behavior changes.

## Submitting a Pull Request

1. Create a feature branch:
git checkout -b feature/my-change

Code
2. Commit your changes with clear messages.
3. Push your branch:
git push origin feature/my-change

Code
4. Open a Pull Request on GitHub.

## Code Style

- Use Python 3.10+ features.
- Keep functions small and readable.
- Avoid unnecessary dependencies.
- Prefer pure functions where possible.

## Reporting Issues

If you find a bug or have a feature request, open an issue on GitHub with:

- A clear description
- Steps to reproduce (if applicable)
- Expected vs actual behavior
- Logs or screenshots if helpful

Thanks again for contributing!
