# Manim122

A CMU 15-122 TA project for creating educational animations and slides using Manim.

## Quick Setup

### 1. Install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Install Manim + Dependencies

```bash
uv venv
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

Install the Manim Sideview extension from the VS Code marketplace.

### 5. Configure Manim Sideview for Virtual Environment

To make Manim Sideview use your project's virtual environment:

1. Open VS Code settings (Cmd/Ctrl + ,)
2. Search for "manim sideview"
3. Find "Manim-sideview: Executable Path"
4. Set it to: `${workspaceFolder}/.venv/bin/manim`

## Project Structure

```
manim122/
├── pyproject.toml          # uv configuration
├── .vscode/
│   └── settings.json       # VS Code workspace settings
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

### Using Manim Sideview

With the extension properly configured:

1. Open any `.py` file with Manim scenes
2. Right-click in the editor
3. Select "Manim Sideview: Show preview"
4. The preview will use your virtual environment and have access to `manim122lib`

## Troubleshooting

### Manim Sideview Issues

**"ModuleNotFoundError: No module named 'manim'"**

-   Ensure Manim Sideview is configured to use your virtual environment (see step 5 above)
-   Verify `manim122lib` is installed: `uv run python -c "import manim122lib; print('OK')"`

## Contributing

Each precept folder contains animations and slides for that week's material. Use the shared `manim122lib` for common components and styling to maintain consistency across all precepts.
