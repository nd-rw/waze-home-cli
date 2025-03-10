# CLAUDE.md - Agent Instructions

## Commands

- Install dependencies: `uv pip install -e .`
- Run CLI: `python -m waze_home`
- Run specific command: `python -m waze_home [command]`
- Lint: `ruff check .`
- Format: `ruff format .`
- Typecheck: `mypy .`
- Test: `pytest`
- Test single file: `pytest path/to/test.py -v`

## Code Style

- Use Python 3.10+ with type annotations
- Follow PEP 8 and Ruff linting rules
- Use snake_case for functions, variables, modules
- Use PascalCase for classes
- Organize imports: stdlib, third-party, local
- Prefer pathlib over os.path
- Use asyncio for concurrent operations
- Document public APIs with docstrings
- Handle errors with appropriate exception classes
- Use click for CLI interface

## Variables

"Home" = '91 Abbett St, Scarborough WA 6019'
"Work" = '11 Mount St, Perth WA 6000'
