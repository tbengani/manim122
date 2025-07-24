# Manim122

A CMU 15-122 TA project for creating educational animations and slides using Manim.

## Quick Setup

### 1. Install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Install Manim + Dependencies

```bash
uv sync
```

### 3. Install LaTeX

**macOS:**

```bash
brew install --cask mactex
```

**Ubuntu/Debian:**

```bash
sudo apt install texlive-full
```

**Windows:**
Install MiKTeX from https://miktex.org/

### 4. Install Manim Sideview VS Code Extension

Install from here: https://marketplace.visualstudio.com/items?itemName=Rickaym.manim-sideview

## Project Structure

```
manim122/
├── pyproject.toml          # uv configuration
├── manim122lib/            # Shared library code
│   ├── __init__.py
│   └── ...                 # Common utilities and styles
├── pc01/                   # Precept 1 materials
├── pc02/                   # Precept 2 materials
├── ...
└── pc13/                   # Precept 13 materials
```

## Usage

Navigate to any precept folder and run:

```bash
uv run manim scene.py SceneName -pql
```

For slides:

```bash
uv run manim-slides SceneName scene.py
```

## Contributing

Each precept folder contains animations and slides for that week's material. Use the shared `manim122lib` for common components and styling to maintain consistency across all precepts.
