from agents import Runner
from ai_reviewer.reviewer import reviewer
import json


def build_prompt(summary):
    return f"""
You are a Senior Software Engineer performing a professional code review.

The following JSON contains the complete repository analysis.

It includes:
- Repository statistics
- Per-file AST analysis
- Security scan results

Rules:
- Base your review ONLY on this data.
- Do NOT invent issues.
- Mention file names whenever possible.
- If no issues are present, say so.
- You should not repeat your analysis again and again.

Return your response in Markdown using only the following sections:

# Overall Score (out of 10)

# Executive Summary

# Strengths

# Weaknesses

# Security Analysis

# Recommendations

Repository Analysis:
{json.dumps(summary, indent=2)}
"""


async def review(summary):
    prompt = build_prompt(summary)

    result = await Runner.run(
        reviewer,
        prompt
    )

    return result.final_output