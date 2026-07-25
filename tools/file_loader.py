from pathlib import Path

IGNORE_DIRS = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    "node_modules",
    "site-packages",
    ".pytest_cache",
    ".mypy_cache"
}

def get_python_files(repo_path):
    repo = Path(repo_path)
    python_files = []

    for file in repo.rglob("*.py"):
        if any(part in IGNORE_DIRS for part in file.parts):
            continue
        python_files.append(file)

    return python_files