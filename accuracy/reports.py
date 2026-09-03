from .scoring import Evaluation

def markdown_report(title: str, evaluation: Evaluation) -> str:
    lines = [f"# {title}", "", f"**Total:** {evaluation.total}/40 ({evaluation.percentage:.0f}%)", f"**Classification:** {evaluation.classification}", "", "## Dimension scores", ""]
    for name, score in evaluation.scores.items():
        lines.append(f"- **{name}:** {score}/5")
    if evaluation.critical_flags:
        lines += ["", "## Critical flags", ""] + [f"- {x}" for x in evaluation.critical_flags]
    return "\n".join(lines) + "\n"
