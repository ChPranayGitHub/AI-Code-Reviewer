import asyncio
import gradio as gr

from tools.github_tool import clone_repo
from tools.file_loader import get_python_files
from tools.ast_tool import analyze_file
from tools.security_tool import scan_file
from tools.summary_tool import summarize_ast, summarize_security
from ai_reviewer.review import review
from report_generator import save_markdown


def analyze_repository(repo_url):
    try:
        repo = clone_repo(repo_url)

        files = get_python_files(repo)

        ast_results = []
        security_results = []

        for file in files:
            ast_results.append(analyze_file(file))
            security_results.append(scan_file(file))

        ast_summary = summarize_ast(ast_results)
        security_summary = summarize_security(security_results)

        overall_summary = {
            "ast": {
                "summary": ast_summary,
                "files": ast_results
            },
            "security": {
                "summary": security_summary,
                "files": security_results
            }
        }
        report = asyncio.run(review(overall_summary))

        markdown_path = save_markdown(report)

        return report, markdown_path

    except Exception as e:
        return f"Error:\n\n{str(e)}", None


demo = gr.Interface(
    fn=analyze_repository,
    inputs=gr.Textbox(
        label="GitHub Repository URL",
        placeholder=""
    ),
    outputs=[
        gr.Markdown(label="AI Code Review"),
        gr.File(label="Download Markdown Report")
    ],
    title="AI Code Reviewer",
    description="Analyze any public GitHub Python repository using AST analysis, security scanning, and GPT.",
    flagging_mode="never" 
)

if __name__ == "__main__":
    demo.launch()