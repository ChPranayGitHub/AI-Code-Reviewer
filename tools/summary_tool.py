def summarize_ast(ast_results):
    summary = {
        "files": 0,
        "functions": 0,
        "classes": 0,
        "large_functions": 0,
        "too_many_parameters": 0,
        "missing_docstrings": 0,
        "large_classes": 0
    }

    for result in ast_results:
        summary["files"] += 1
        summary["functions"] += len(result["functions"])
        summary["classes"] += len(result["classes"])
        summary["large_functions"] += len(result["large_functions"])
        summary["too_many_parameters"] += len(result["too_many_parameters"])
        summary["missing_docstrings"] += len(result["missing_docstrings"])
        summary["large_classes"] += len(result["large_classes"])

    return summary


def summarize_security(security_results):
    summary = {
        "critical_count": 0,
        "high_count": 0,
        "critical": [],
        "high": []
    }

    for result in security_results:
        summary["critical_count"] += len(result["critical"])
        summary["high_count"] += len(result["high"])

        summary["critical"].extend(result["critical"])
        summary["high"].extend(result["high"])

    return summary