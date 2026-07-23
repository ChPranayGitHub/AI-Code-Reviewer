from agents import Agent, Runner
from dotenv import load_dotenv

load_dotenv()

reviewer = Agent(
    name="Senior Code Reviewer",
    model="gpt-5-nano",
    instructions="""
You are a senior software engineer.

You receive AST analysis and security findings of a GitHub repository.

Write a professional code review.

Focus on:
- Code quality
- Maintainability
- Security
- Architecture
- Best practices

Give:
1. Overall Score (out of 10)
2. Strengths
3. Weaknesses
4. Recommendations

Do NOT invent issues that are not present.
"""
)