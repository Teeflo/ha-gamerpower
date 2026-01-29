# Contributing to GamerPower Integration

Thank you for your interest in contributing to the GamerPower Home Assistant integration!

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/Teeflo/ha-gamerpower.git
   cd ha-gamerpower
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # or
   .\venv\Scripts\activate  # Windows
   ```

3. Install development dependencies:
   ```bash
   pip install ruff pytest homeassistant
   ```

## Code Style

We use [Ruff](https://github.com/astral-sh/ruff) for linting and formatting.

- **Check code**: `ruff check custom_components/gamerpower`
- **Fix issues**: `ruff check --fix custom_components/gamerpower`
- **Format code**: `ruff format custom_components/gamerpower`

## Guidelines

- All code must be fully async (no blocking I/O)
- Use type hints on all functions
- Follow Google-style docstrings
- Keep strings translatable via `strings.json`
- Test your changes locally before submitting

## Pull Requests

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Run linting: `ruff check custom_components/gamerpower`
5. Commit with conventional commits: `git commit -m "feat: add new feature"`
6. Push and create a Pull Request

## Questions?

Open an issue on GitHub if you have questions or need help.
