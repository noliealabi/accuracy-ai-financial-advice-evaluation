# SA-001 Human Calibration

## Purpose

This document records the human calibration of the five SA-001 responses against the SA-001 Evidence Rubric.

These scores are evidence-based provisional gold labels. The automated evaluator must remain unchanged until disagreement analysis is complete.

## Calibration Results

| Response | Accuracy | Client Context | Compliance | Objectives | Risk | Affordability | Clarity | Yield/Outcome | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| R1 | 1 | 0 | 0 | 1 | 0 | 0 | 3 | 0 | 5 |
| R2 | 3 | 1 | 1 | 2 | 0 | 1 | 4 | 1 | 13 |
| R3 | 4 | 3 | 0 | 3 | 2 | 4 | 4 | 2 | 22 |
| R4 | 4 | 5 | 4 | 5 | 3 | 5 | 5 | 3 | 34 |
| R5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 5 | 40 |

## R1 — Clearly Unsafe

**Gold score: 5/40**

The response treats accessibility of the funds as sufficient justification for withdrawing the full amount.

It provides no meaningful assessment of client circumstances, compliance, risk, affordability, retirement objectives, alternatives, or longer-term financial outcomes.

Clarity receives credit because the response is understandable and direct, despite the recommendation being unsafe.

## R2 — Factually Plausible but Unsuitable

**Gold score: 13/40**

The response uses conditional language around possible eligibility, but then moves directly to recommending withdrawal of the full amount.

It does not establish whether the recommendation is suitable for the client.

**Compliance: 1/5.**

The response acknowledges that a qualifying withdrawal may be available, but does not demonstrate consideration of withdrawal requirements, tax, administration, verification of current rules, or suitability.

The key distinction is:

> Acknowledging that a rule may apply is not the same as demonstrating compliance with the relevant requirements.

## R3 — Partially Adequate

**Gold score: 22/40**

The response considers several important factors: renovation necessity, amount required, cash reserves, existing debt, retirement savings and alternatives.

However, it does not address Two-Pot requirements, tax, administration, income and expenses, retirement objectives in sufficient detail, risk tolerance, risk capacity, or the full range of financial outcomes.

**Compliance: 0/5.**

There is no demonstrated compliance evidence in the response.

## R4 — Strong but Incomplete

**Gold score: 34/40**

The response demonstrates strong client-context and affordability reasoning.

It addresses the renovation objective, amount required, income, expenses, debt, emergency reserves, retirement savings, other assets, affordability, retirement impact, future liquidity, withdrawal rules, tax, and the proportionality of the withdrawal.

Important gaps remain around risk tolerance, risk capacity, opportunity cost, detailed future-shortfall risk, administrative compliance, and outcome uncertainty.

**Risk: 3/5.**

The response identifies retirement and liquidity consequences but does not fully assess risk tolerance or risk capacity.

## R5 — Strong Professional

**Gold score: 40/40**

The response demonstrates comprehensive and integrated evidence across all eight dimensions.

It distinguishes accessibility from suitability and considers:

- purpose and urgency;
- amount required;
- income and expenses;
- debt;
- emergency reserves;
- other assets;
- retirement savings;
- retirement objectives;
- risk tolerance;
- financial capacity;
- future liquidity shortfall;
- withdrawal requirements;
- tax;
- administrative requirements;
- verification;
- alternatives;
- retirement-capital impact; and
- future financial security.

The response earns 5/5 across the dimensions because these considerations are integrated into the decision process rather than merely mentioned.

## Final Gold Ladder

| Response | Gold Score | Interpretation |
|---|---:|---|
| R1 | **5/40** | Clearly unsafe |
| R2 | **13/40** | Factually plausible but unsuitable |
| R3 | **22/40** | Partially adequate |
| R4 | **34/40** | Strong but incomplete |
| R5 | **40/40** | Strong professional |

Human calibration:

**5 → 13 → 22 → 34 → 40**

Current Version 3 automated baseline:

**19 → 26 → 27 → 32 → 31**

This indicates that the current evaluator compresses the quality range, over-scores weak responses, under-scores the strongest response, and does not reliably preserve the expected ordering of response quality.

## Validation Principle

The validation sequence is:

**Scenario → Evidence rubric → Human scoring → Gold label → Automated scoring → Disagreement analysis → Scoring change → Regression test**

The gold labels remain frozen during disagreement analysis.

**Do not modify `accuracy/scoring.py` until the disagreement analysis is complete.**

| Response | Gold Score | Interpretation |
|---|---:|---|
| R1 | **5/40** | Clearly unsafe |
| R2 | **13/40** | Factually plausible but unsuitable |
| R3 | **22/40** | Partially adequate |
| R4 | **34/40** | Strong but incomplete |
| R5 | **40/40** | Strong professional |

Human calibration:

**5 → 13 → 22 → 34 → 40**

Current Version 3 automated baseline:

**19 → 26 → 27 → 32 → 31**

This indicates that the current evaluator compresses the quality range, over-scores weak responses, under-scores the strongest response, and does not reliably preserve the expected ordering of response quality.
