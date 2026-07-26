import os
from datetime import datetime


def save_markdown(report):
    """
    Save the review report as a Markdown file.

    Args:
        report (str): The review report content.

    Returns:
        str: The path to the saved Markdown file.
    """
    os.makedirs("reports", exist_ok=True)

    path = os.path.join("reports", f"review_{datetime.now().strftime('%Y%m%d%H%M%S')}.md")

    with open(path, "w", encoding="utf-8") as f:
        f.write(report)

    return path