from pathlib import Path

def get_python_files(repo_path):
    repo = Path(repo_path)

    python_files = []

    for file in repo.rglob("*.py"):
        python_files.append(file)

    return python_files