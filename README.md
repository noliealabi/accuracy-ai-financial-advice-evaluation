# A.C.C.U.R.A.C.Y. AI Financial Advice Evaluation Framework — v3.0 🇿🇦

A human-centred evaluation framework for assessing AI-generated financial advice across **Accuracy, Client Context, Compliance, Objectives, Risk, Affordability, Clarity, and Yield/Outcome alignment**.

> **Important:** This is an AI evaluation and research project using synthetic scenarios. It is not financial, legal or tax advice.

## Version 3 — South African Benchmark

Version 3 adds **81 synthetic South African scenarios** covering:

- Two-Pot retirement-system decisions
- Retirement planning and retirement income
- Tax-Free Savings Accounts (TFSA)
- JSE/local investment concentration
- Rand and offshore diversification
- Insurance and income protection
- Medical-cover decisions
- Debt and affordability
- Cash-flow and emergency funds
- Education planning
- Estate planning, wills and beneficiaries
- Cross-border/residency questions
- Financial-services conduct and fact-finding
- Treating Customers Fairly considerations

## Repository structure

```text
app/                  Streamlit demonstration app
accuracy/             Scoring and report-generation engine
data/                 Structured benchmark datasets
docs/                 Methodology and South African context
scenarios_sa/         Individual South African scenario cards
tests/                Automated tests
.github/workflows/    GitHub Actions CI
```

## A.C.C.U.R.A.C.Y. dimensions

| Dimension | What it tests |
|---|---|
| A — Accuracy | Factual correctness and avoidance of misleading claims |
| C — Client Context | Whether material client facts are considered |
| C — Compliance | Regulatory, disclosure and professional-conduct awareness |
| U — Objectives | Alignment with the client's actual goals |
| R — Risk | Risk tolerance, capacity, horizon and downside awareness |
| A — Affordability | Cash flow, debt, liquidity and sustainability |
| C — Clarity | Transparent assumptions, trade-offs and understandable communication |
| Y — Yield/Outcome | Whether the proposed approach plausibly supports the intended outcome |

Each dimension is scored from **0–5**, giving a maximum raw score of **40/40**.

## Quick start

```bash
python -m venv .venv
# Windows
.venv\\Scripts\\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
python -m unittest discover -s tests -v
streamlit run app/streamlit_app.py
```

## Benchmark files

- `data/benchmark_sa.json` — 81 structured South African scenarios
- `data/benchmark_sa.csv` — spreadsheet-ready version
- `scenarios_sa/` — individual Markdown scenario cards

## Example evaluation workflow

1. Present an AI-generated financial response.
2. Evaluate it against each A.C.C.U.R.A.C.Y. dimension.
3. Flag critical failures such as guarantees, unsupported legal/tax claims or material suitability failures.
4. Calculate the overall score.
5. Determine whether human review is required.
6. Record the reasoning and recommended improvement.

## South African context

The benchmark is designed around South African financial-planning contexts. Live regulatory and tax rules must always be verified against authoritative sources before use in real advice.

## Roadmap

- **v1:** Core framework
- **v2:** General benchmark and evaluation tooling
- **v3:** South African jurisdiction-specific benchmark 🇿🇦
- **v4:** LLM-connected automated evaluation engine
- **v5:** Model comparison, analytics and evaluator calibration

## Portfolio positioning

This project demonstrates domain expertise in wealth management and financial planning combined with AI evaluation, prompt design, rubric design, critical review, structured benchmarking, Python and automated testing.

## Disclaimer

A.C.C.U.R.A.C.Y. is an AI evaluation/research framework. It does not provide personalised financial advice and should not replace a qualified financial adviser, legal professional or tax practitioner. Synthetic benchmark scenarios are not recommendations.
