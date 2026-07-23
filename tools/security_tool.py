import ast
import re


SECRET_PATTERNS = {
    # ---------- Keyword-based ----------
    "Hardcoded Password": r'(?i)(password|passwd|pwd)\s*=\s*["\'][^"\']+["\']',
    "API Key": r'(?i)(api[_-]?key)\s*=\s*["\'][^"\']+["\']',
    "Secret Key": r'(?i)(secret[_-]?key)\s*=\s*["\'][^"\']+["\']',
    "Access Token": r'(?i)(token|access_token)\s*=\s*["\'][^"\']+["\']',

    # ---------- Known Secret Formats ----------
    "OpenAI API Key": r"sk-(proj-)?[A-Za-z0-9_-]{20,}",
    "GitHub Personal Access Token": r"gh[pousr]_[A-Za-z0-9]{36,}",
    "AWS Access Key": r"AKIA[0-9A-Z]{16}",
    "Google API Key": r"AIza[0-9A-Za-z\-_]{35}",
    "Hugging Face Token": r"hf_[A-Za-z0-9]{20,}",
    "JWT Token": r"eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+",

}

def scan_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        source = f.read()

    tree = ast.parse(source)

    findings = {
        "file": str(file_path),
        "critical": [],
        "high": []
    }


    for node in ast.walk(tree):

        if isinstance(node, ast.Call):

            # eval(), exec()
            if isinstance(node.func, ast.Name):

                if node.func.id == "eval":
                    findings["critical"].append({
                        "issue": "Use of eval()",
                        "line": node.lineno
                    })

                elif node.func.id == "exec":
                    findings["critical"].append({
                        "issue": "Use of exec()",
                        "line": node.lineno
                    })

            # os.system(), subprocess.run(), pickle.loads(), yaml.load()
            elif isinstance(node.func, ast.Attribute):

                if isinstance(node.func.value, ast.Name):
                    full_name = f"{node.func.value.id}.{node.func.attr}"

                    if full_name == "os.system":
                        findings["critical"].append({
                            "issue": "Use of os.system()",
                            "line": node.lineno
                        })

                    elif full_name == "pickle.loads":
                        findings["critical"].append({
                            "issue": "Use of pickle.loads()",
                            "line": node.lineno
                        })

                    elif full_name == "yaml.load":
                        findings["high"].append({
                            "issue": "Use yaml.safe_load() instead of yaml.load()",
                            "line": node.lineno
                        })

                    elif full_name == "subprocess.run":

                        for keyword in node.keywords:
                            if (
                                keyword.arg == "shell"
                                and isinstance(keyword.value, ast.Constant)
                                and keyword.value.value is True
                            ):
                                findings["critical"].append({
                                    "issue": "subprocess.run(shell=True)",
                                    "line": node.lineno
                                })


    lines = source.splitlines()

    for issue, pattern in SECRET_PATTERNS.items():

        regex = re.compile(pattern)

        for line_number, line in enumerate(lines, start=1):

            if regex.search(line):
                findings["high"].append({
                    "issue": issue,
                    "line": line_number
                })

    return findings