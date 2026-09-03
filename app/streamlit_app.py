import json
from pathlib import Path
import streamlit as st
from accuracy.scoring import DIMENSIONS, evaluate
from accuracy.reports import markdown_report

st.set_page_config(page_title="A.C.C.U.R.A.C.Y. v3", page_icon="🇿🇦", layout="wide")
st.title("A.C.C.U.R.A.C.Y. AI Financial Advice Evaluator")
st.caption("Version 3 — South African benchmark demonstration")

st.warning("Synthetic evaluation tool for research/QA. Not personalised financial advice.")
scenario = st.text_area("Client scenario", height=160, placeholder="Paste a client scenario here...")
response = st.text_area("AI-generated financial response", height=220, placeholder="Paste the AI response you want to evaluate...")

st.subheader("Score the response")
scores = {}
cols = st.columns(4)
for i, dim in enumerate(DIMENSIONS):
    with cols[i % 4]:
        scores[dim] = st.slider(dim, 0, 5, 3, key=dim)
flags_text = st.text_area("Critical flags (one per line)", placeholder="Example: Unsupported guarantee\nExample: Material tax claim requires verification")

if st.button("Evaluate response", type="primary"):
    evaluation = evaluate(scores, [x.strip() for x in flags_text.splitlines() if x.strip()])
    st.metric("A.C.C.U.R.A.C.Y. score", f"{evaluation.total}/40")
    st.write(f"**Classification:** {evaluation.classification}")
    st.progress(evaluation.percentage / 100)
    st.subheader("Evaluation report")
    report = markdown_report("A.C.C.U.R.A.C.Y. Evaluation", evaluation)
    st.markdown(report)
    st.download_button("Download Markdown report", report, file_name="accuracy_evaluation.md")
