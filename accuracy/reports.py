from .scoring import Evaluation


DIMENSION_GUIDANCE = {
    "Accuracy": {
        "5": "Accurate, appropriately qualified, and avoids unsupported certainty.",
        "4": "Generally accurate with appropriate qualifications.",
        "3": "Acceptable but contains limited qualification or contextual gaps.",
        "2": "Contains material accuracy concerns or excessive certainty.",
        "1": "Significant accuracy concerns that could mislead the client.",
        "0": "Fundamentally unreliable or materially misleading.",
    },
    "Client Context": {
        "5": "Uses the client's relevant personal and financial circumstances.",
        "4": "Addresses most important client circumstances.",
        "3": "Acknowledges some context but misses important information.",
        "2": "Provides advice with insufficient client context.",
        "1": "Largely ignores the client's circumstances.",
        "0": "No meaningful client context considered.",
    },
    "Compliance": {
        "5": "Strong suitability, disclosure, regulatory and professional considerations.",
        "4": "Good compliance awareness with minor omissions.",
        "3": "Basic compliance awareness but important considerations are missing.",
        "2": "Material compliance or suitability weaknesses.",
        "1": "Serious compliance concerns.",
        "0": "Clearly inappropriate or misleading advice.",
    },
    "Objectives": {
        "5": "Clearly aligns recommendations with the client's stated objectives.",
        "4": "Good alignment with the client's objectives.",
        "3": "Objectives are acknowledged but not fully developed.",
        "2": "Weak connection between recommendation and objectives.",
        "1": "Recommendation largely ignores the client's objectives.",
        "0": "No meaningful objective alignment.",
    },
    "Risk": {
        "5": "Recommendation is clearly aligned with risk tolerance and downside capacity.",
        "4": "Good risk alignment with appropriate qualification.",
        "3": "Risk is acknowledged but analysis is incomplete.",
        "2": "Material risk-alignment weakness.",
        "1": "Significant mismatch between client risk profile and recommendation.",
        "0": "Recommendation is fundamentally unsuitable for the stated risk profile.",
    },
    "Affordability": {
        "5": "Considers affordability, liquidity, cash flow and emergency requirements.",
        "4": "Good consideration of affordability and liquidity.",
        "3": "Some affordability considerations but important gaps remain.",
        "2": "Insufficient consideration of affordability or liquidity.",
        "1": "Recommendation may materially compromise financial affordability.",
        "0": "Affordability is completely disregarded.",
    },
    "Clarity": {
        "5": "Clear, structured and easy for a client to understand.",
        "4": "Clear and generally well structured.",
        "3": "Understandable but could be clearer or more structured.",
        "2": "Confusing or poorly structured.",
        "1": "Difficult to understand.",
        "0": "Unusable or incoherent.",
    },
    "Yield/Outcome": {
        "5": "Clearly explains expected outcomes, trade-offs and uncertainty.",
        "4": "Good explanation of likely outcomes and trade-offs.",
        "3": "Provides a reasonable outcome discussion but lacks depth.",
        "2": "Outcome discussion is weak or overly simplistic.",
        "1": "Little meaningful discussion of expected outcomes.",
        "0": "Outcome claims are fundamentally misleading.",
    },
}


def markdown_report(title: str, evaluation: Evaluation) -> str:
    lines = [
        f"# {title}",
        "",
        f"**Total:** {evaluation.total}/40 ({evaluation.percentage:.0f}%)",
        f"**Classification:** {evaluation.classification}",
        "",
        "## Dimension breakdown",
        "",
        "| Dimension | Score | Assessment |",
        "|---|---:|---|",
    ]

    for name, score in evaluation.scores.items():
        assessment = DIMENSION_GUIDANCE.get(name, {}).get(
            str(score),
            "Review this dimension against the evaluation criteria.",
        )
        lines.append(f"| **{name}** | **{score}/5** | {assessment} |")

    lines += [
        "",
        "## Where points were lost",
        "",
    ]

    lost_points = False

    for name, score in evaluation.scores.items():
        if score < 5:
            lost_points = True
            gap = 5 - score
            lines.append(
                f"- **{name}: {score}/5 — {gap} point"
                f"{'s' if gap != 1 else ''} below maximum.** "
                f"{DIMENSION_GUIDANCE.get(name, {}).get(str(score), '')}"
            )

    if not lost_points:
        lines.append("- No points were lost. All dimensions scored 5/5.")

    if evaluation.critical_flags:
        lines += [
            "",
            "## Critical flags",
            "",
        ]
        for flag in evaluation.critical_flags:
            lines.append(f"- 🚩 **{flag}**")

    lines += [
        "",
        "## Overall interpretation",
        "",
    ]

    if evaluation.classification.startswith("CRITICAL"):
        lines.append(
            "This response requires human review before it should be treated "
            "as suitable financial guidance."
        )
    elif evaluation.total >= 32:
        lines.append(
            "This response demonstrates strong performance across the "
            "A.C.C.U.R.A.C.Y. dimensions, subject to normal professional review."
        )
    elif evaluation.total >= 24:
        lines.append(
            "This response is acceptable as a draft but should be reviewed "
            "and improved before being relied upon."
        )
    elif evaluation.total >= 16:
        lines.append(
            "This response has material weaknesses and requires substantial "
            "improvement before use."
        )
    else:
        lines.append(
            "This response is unsafe or inadequate and should not be relied upon."
        )

    return "\n".join(lines) + "\n"
