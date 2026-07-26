import ast


def analyze_file(file_path):
    """Analyze a Python file and return its AST analysis"""
    with open(file_path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read())

    result = {
        "file": str(file_path),
        "functions": [],
        "classes": [],
        "large_functions": [],
        "too_many_parameters": [],
        "missing_docstrings": [],
        "large_classes": []
    }

    for node in ast.walk(tree):

        if isinstance(node, ast.FunctionDef):

            args = len(node.args.args)

            lines = (
                node.end_lineno - node.lineno + 1
                if hasattr(node, "end_lineno")
                else 0
            )

            has_docstring = ast.get_docstring(node) is not None

            result["functions"].append({
                "name": node.name,
                "args": args,
                "lines": lines,
                "has_docstring": has_docstring
            })

            if lines > 50:
                result["large_functions"].append(node.name)

            if args > 5:
                result["too_many_parameters"].append(node.name)

            if not has_docstring:
                result["missing_docstrings"].append(node.name)


        elif isinstance(node, ast.ClassDef):

            methods = sum(
                isinstance(n, ast.FunctionDef)
                for n in node.body
            )

            result["classes"].append({
                "name": node.name,
                "methods": methods
            })

            if methods > 10:
                result["large_classes"].append(node.name)

    return result