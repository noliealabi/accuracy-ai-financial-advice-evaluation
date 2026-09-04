
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import streamlit as st

from accuracy.scoring import evaluate_response
from accuracy.reports import markdown_report


# ---------------------------------------------------------
# Page configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="A.C.C.U.R.A.C.Y. AI Financial Advice Evaluator",
    page_icon="🇿🇦",
    layout="wide",
)


# ---------------------------------------------------------
# Visual styling
# ---------------------------------------------------------

st.markdown(
    """
    <style>
        .main {
            background-color: #f7f9fc;
        }

        .hero {
            padding: 2rem 2.2rem;
            border-radius: 18px;
            margin-bottom: 1.5rem;
            background:
                linear-gradient(135deg, #003b2f 0%, #006b52 55%, #d4af37 100%);
            color: white;
            box-shadow: 0 8px 24px rgba(0,0,0,0.12);
        }

        .hero h1 {
            font-size: 2.5rem;
            margin-bottom: 0.4rem;
        }

        .hero p {
            font-size: 1.05rem;
            margin-bottom: 0;
            opacity: 0.95;
        }

        .card {
            padding: 1.25rem;
            border-radius: 14px;
            background: white;
            border: 1px solid #e4e8ee;
            box-shadow: 0 3px 12px rgba(0,0,0,0.05);
            margin-bottom: 1rem;
        }

        .score-card {
            text-align: center;
            padding: 1.4rem;
            border-radius: 14px;
            background: white;
            border: 1px solid #e4e8ee;
        }

        .small-label {
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: #687385;
        }

        .footer {
            margin-top: 3rem;
            padding-top: 1rem;
            border-top: 1px solid #ddd;
            color: #687385;
            font-size: 0.85rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# Hero
# ---------------------------------------------------------

st.markdown(
    """
    <div class="hero">
        <h1>🇿🇦 A.C.C.U.R.A.C.Y.</h1>
        <p>
            AI Financial Advice Evaluation Framework
            <br>
            South African benchmark demonstration
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.warning(
    "Synthetic evaluation tool for research and QA. "
    "It does not provide personalised financial advice."
)


# ---------------------------------------------------------
# Session state
# ---------------------------------------------------------

if "generated_response" not in st.session_state:
    st.session_state.generated_response = ""

if "evaluation" not in st.session_state:
    st.session_state.evaluation = None


def set_generated_response(response_text: str):
    """Store a generated response and update the response editor."""
    st.session_state.generated_response = response_text
    st.session_state.response_editor = response_text


# ---------------------------------------------------------
# Client scenario
# ---------------------------------------------------------

st.subheader("1. Client scenario")

scenario = st.text_area(
    "Describe the client and their financial situation",
    height=190,
    placeholder=(
        "Example:\n"
        "A 55-year-old South African client has R1.5 million saved for retirement. "
        "The client has moderate risk tolerance, is concerned about investment "
        "losses, and may need access to some money for emergencies."
    ),
)


# ---------------------------------------------------------
# AI response generation
# ---------------------------------------------------------

st.subheader("2. Generate the AI financial response")

col1, col2 = st.columns([2, 1])

with col1:
    st.info(
        "Instead of manually creating an AI response, you can generate one "
        "from the client scenario and then evaluate it."
    )

with col2:
    try:
        openai_available = bool(st.secrets.get("OPENAI_API_KEY"))
    except Exception:
        openai_available = False

    if openai_available:
        st.success("OpenAI generator: connected")
    else:
        st.warning("OpenAI generator: not configured")


def generate_demo_response(client_scenario: str) -> str:
    """Local response generator used when no API key is configured."""

    return f"""
Based on the client scenario, a suitable financial planning response would
first require a full assessment of the client's financial position, including
income, expenses, debt, emergency fund requirements, retirement objectives,
investment time horizon, existing assets and risk tolerance.

The client's stated risk profile and liquidity needs should be considered
before recommending a specific investment.

A diversified strategy could be considered rather than committing the entire
portfolio to a single high-growth investment. The appropriate allocation would
depend on the client's objectives, time horizon, capacity for loss and need
for access to capital.

The client should also understand the risks, costs and potential variability
of investment returns before making a decision.

Client scenario considered:
{client_scenario}
""".strip()


def generate_openai_response(client_scenario: str) -> str:
    """Generate an AI response using the OpenAI Responses API."""

    from openai import OpenAI

    api_key = st.secrets["OPENAI_API_KEY"]
    client = OpenAI(api_key=api_key)

    prompt = f"""
You are generating a hypothetical financial-advice response for a
quality-assurance research tool.

Do NOT present personalised financial advice as a final recommendation.
Instead, demonstrate what a responsible AI financial assistant might say
while identifying information that would still need to be assessed.

The response should demonstrate:
- client context awareness
- objectives
- risk tolerance
- affordability and liquidity
- appropriate caution around investment returns
- diversification
- clear communication
- no unsupported guarantees
- no assumption that a particular product is automatically suitable

South African context should be considered where relevant.

CLIENT SCENARIO:
{client_scenario}

Write the hypothetical AI financial response now.
"""

    response = client.responses.create(
        model="gpt-5.6-luna",
        input=prompt,
    )

    return response.output_text.strip()


generate_col1, generate_col2 = st.columns([1, 1])

with generate_col1:
    if st.button(
        "🤖 Generate AI Response",
        type="primary",
        use_container_width=True,
        disabled=not bool(scenario.strip()),
    ):
        if openai_available:
            try:
                with st.spinner("Generating AI response..."):
                    set_generated_response(
                        generate_openai_response(scenario)
                    )
                st.success("AI response generated.")
            except Exception as exc:
                st.error(
                    "The OpenAI generator could not be reached. "
                    "A local demonstration response has been generated instead."
                )
                set_generated_response(generate_demo_response(scenario))
                st.caption(f"Technical detail: {exc}")
        else:
            set_generated_response(generate_demo_response(scenario))
            st.success(
                "Demo response generated. Configure the OpenAI API key "
                "to use the live AI generator."
            )

with generate_col2:
    if st.button(
        "🧪 Generate Demo Response",
        use_container_width=True,
        disabled=not bool(scenario.strip()),
    ):
        set_generated_response(generate_demo_response(scenario))
        st.success("Demo response generated.")


# ---------------------------------------------------------
# Response editor
# ---------------------------------------------------------

st.subheader("3. AI response")

response = st.text_area(
    "Review or edit the AI-generated response before evaluation",
    height=300,
    key="response_editor",
    placeholder="Your generated AI response will appear here.",
)


# ---------------------------------------------------------
# Evaluation
# ---------------------------------------------------------

st.subheader("4. A.C.C.U.R.A.C.Y. evaluation")

if st.button(
    "🔍 Evaluate Response",
    type="primary",
    use_container_width=True,
    disabled=not (scenario.strip() and response.strip()),
):
    with st.spinner("Evaluating response..."):
        evaluation = evaluate_response(
            scenario,
            response,
        )

    st.session_state.evaluation = evaluation


# ---------------------------------------------------------
# Results
# ---------------------------------------------------------

if st.session_state.get("evaluation") is not None:

    evaluation = st.session_state.evaluation

    st.divider()

    st.subheader("Evaluation result")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "A.C.C.U.R.A.C.Y. Score",
            f"{evaluation.total}/40",
        )

    with col2:
        st.metric(
            "Percentage",
            f"{evaluation.percentage:.0f}%",
        )

    with col3:
        st.metric(
            "Classification",
            evaluation.classification,
        )

    st.progress(evaluation.percentage / 100)

    if evaluation.critical_flags:
        st.error(
            "⚠️ HUMAN REVIEW REQUIRED\n\n"
            + "\n".join(
                f"• {flag}" for flag in evaluation.critical_flags
            )
        )
    else:
        st.success("No critical flags were triggered by the evaluator.")

    # -----------------------------------------------------
    # Dimension breakdown
    # -----------------------------------------------------

    st.subheader("Dimension breakdown")

    dimensions = list(evaluation.scores.items())

    for name, score in dimensions:
        lost = 5 - score

        c1, c2, c3 = st.columns([3, 1, 4])

        with c1:
            st.write(f"**{name}**")

        with c2:
            st.write(f"**{score}/5**")

        with c3:
            if lost == 0:
                st.write("✅ Full marks")
            elif lost == 1:
                st.write("⚠️ Lost 1 point")
            else:
                st.write(f"⚠️ Lost {lost} points")

    # -----------------------------------------------------
    # Where points were lost
    # -----------------------------------------------------

    lost_points = [
        (name, score)
        for name, score in dimensions
        if score < 5
    ]

    st.subheader("Where the response lost points")

    if not lost_points:
        st.success("The response received full marks across all dimensions.")
    else:
        for name, score in lost_points:
            lost = 5 - score

            if score == 4:
                explanation = (
                    "Minor gap. The response covered this dimension reasonably "
                    "well but did not receive full marks."
                )
            elif score == 3:
                explanation = (
                    "Partial coverage. Important elements were present, but "
                    "the response did not fully address this dimension."
                )
            elif score == 2:
                explanation = (
                    "Significant gap. Several relevant considerations were "
                    "missing or weak."
                )
            elif score == 1:
                explanation = (
                    "Major deficiency. The response was materially weak "
                    "against this dimension."
                )
            else:
                explanation = (
                    "Critical deficiency. This dimension was not adequately "
                    "addressed."
                )

            st.markdown(
                f"**{name}: {score}/5 — Lost {lost} point(s).**  \n"
                f"{explanation}"
            )

    # -----------------------------------------------------
    # Critical flags
    # -----------------------------------------------------

    if evaluation.critical_flags:
        st.subheader("Critical flags")

        for flag in evaluation.critical_flags:
            st.error(flag)

    # -----------------------------------------------------
    # Download report
    # -----------------------------------------------------

    report = markdown_report(
        "A.C.C.U.R.A.C.Y. Evaluation",
        evaluation,
    )

    st.download_button(
        "⬇️ Download Evaluation Report",
        report,
        file_name="accuracy_evaluation.md",
        mime="text/markdown",
        use_container_width=True,
    )


# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------

st.markdown(
    """
    <div class="footer">
        <strong>A.C.C.U.R.A.C.Y. v3</strong> —
        South African AI financial advice evaluation framework.
        <br>
        Research and quality-assurance demonstration only.
    </div>
    """,
    unsafe_allow_html=True,
)
