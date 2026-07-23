import os


def save_markdown(report):
    os.makedirs("reports", exist_ok=True)

    path = os.path.join("reports", "review.md")

    with open(path, "w", encoding="utf-8") as f:
        f.write(report)

    return path