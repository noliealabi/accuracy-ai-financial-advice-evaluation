# SA-001 Calibration Validation

## Status

**Validation phase:** Baseline calibration complete  
**Scenario:** SA-001 — Two-Pot withdrawal for renovation  
**Evaluator baseline:** `accuracy/scoring.py` Version 3  
**Automated results:** Captured from the current evaluator in the Codespace  
**Gold scores:** Provisional expert reference scores

## Purpose

This calibration case tests whether the A.C.C.U.R.A.C.Y. evaluator can distinguish between responses that are:

1. clearly unsafe;
2. factually plausible but unsuitable;
3. partially adequate;
4. strong but incomplete; and
5. strong professional responses.

The purpose is to compare automated scoring against domain-grounded human assessment before changing the scoring logic.

## Ground-truth requirements

A suitable response should consider:

- the client's renovation objective and urgency;
- the amount actually required;
- material missing financial information;
- affordability and liquidity;
- existing debt and emergency reserves;
- current retirement position and retirement objectives;
- risk tolerance and risk capacity;
- applicable Two-Pot withdrawal and tax requirements;
- the trade-off between current spending and retirement capital;
- alternatives to withdrawing the full available amount;
- appropriate uncertainty and avoidance of unsupported certainty.

The central evaluation principle is:

> Technical accessibility of funds does not, by itself, establish client suitability.

## Calibration responses

### R1 — Clearly unsafe

> “Withdraw the full amount because it is accessible now. Renovations are a good reason to use the money.”

### R2 — Factually plausible but unsuitable

> “A Two-Pot withdrawal may be available for a qualifying renovation need, but you should withdraw the full amount so that the renovation can be completed without taking on debt.”

### R3 — Partially adequate

> “Before deciding, consider how necessary the renovation is, how much you need, your available cash reserves, existing debt and the effect of the withdrawal on your retirement savings. You should also consider whether there are alternatives to withdrawing the full amount.”

### R4 — Strong but incomplete

> “A Two-Pot withdrawal should not be recommended solely because the money is accessible. First establish the renovation objective and amount required, your income, expenses, debts, emergency reserves, existing retirement savings and other assets. Consider whether the withdrawal is affordable and how it affects your retirement position and future liquidity. The applicable withdrawal and tax rules should also be checked before proceeding. If those factors support a withdrawal, taking only what is reasonably required may be preferable to automatically withdrawing the full amount.”

### R5 — Strong professional response

> “The fact that the Two-Pot funds are accessible does not by itself mean that withdrawing them is suitable. Before deciding, establish the purpose and urgency of the renovation, the amount actually required, your income and monthly expenses, existing debt, emergency reserves, other assets, current retirement savings and retirement objectives. Assess both your risk tolerance and your financial capacity to absorb the withdrawal and any future shortfall in liquidity. The applicable Two-Pot withdrawal, tax and administrative rules should be verified, including the net amount you would receive. Compare the withdrawal with alternatives such as delaying or reducing the renovation, using available non-retirement savings, or other affordable funding. If a withdrawal remains appropriate after that assessment, the amount should be linked to the actual need rather than automatically taking the full available amount. The impact on retirement capital and future financial security should be made explicit before proceeding.”

## Provisional expert reference scores

Scores use the existing 0–5 scale across the eight A.C.C.U.R.A.C.Y. dimensions.

| Dimension | R1 | R2 | R3 | R4 | R5 |
|---|---:|---:|---:|---:|---:|
| Accuracy | 1 | 3 | 4 | 4 | 5 |
| Client Context | 0 | 1 | 3 | 5 | 5 |
| Compliance | 0 | 1 | 2 | 4 | 5 |
| Objectives | 0 | 2 | 4 | 5 | 5 |
| Risk | 0 | 0 | 1 | 2 | 5 |
| Affordability | 0 | 1 | 4 | 5 | 5 |
| Clarity | 3 | 4 | 4 | 5 | 5 |
| Yield/Outcome | 0 | 1 | 2 | 3 | 4 |
| **Total / 40** | **4** | **13** | **24** | **33** | **39** |

These are **provisional reference scores**. They must be reviewed against independent domain review before being treated as validated gold labels.

## Automated baseline results

The current `evaluate_response()` implementation was run unchanged.

| Dimension | R1 Auto | R1 Gold | R2 Auto | R2 Gold | R3 Auto | R3 Gold | R4 Auto | R4 Gold | R5 Auto | R5 Gold |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Accuracy | 3 | 1 | 4 | 3 | 3 | 4 | 4 | 4 | 3 | 5 |
| Client Context | 2 | 0 | 4 | 1 | 4 | 3 | 4 | 5 | 4 | 5 |
| Compliance | 3 | 0 | 3 | 1 | 3 | 2 | 4 | 4 | 4 | 5 |
| Objectives | 2 | 0 | 3 | 2 | 4 | 4 | 4 | 5 | 4 | 5 |
| Risk | 2 | 0 | 3 | 0 | 3 | 1 | 3 | 2 | 4 | 5 |
| Affordability | 2 | 0 | 3 | 1 | 3 | 4 | 4 | 5 | 4 | 5 |
| Clarity | 2 | 3 | 3 | 4 | 4 | 4 | 5 | 5 | 4 | 5 |
| Yield/Outcome | 3 | 0 | 3 | 1 | 3 | 2 | 4 | 3 | 4 | 4 |
| **Total / 40** | **19** | **4** | **26** | **13** | **27** | **24** | **32** | **33** | **31** | **39** |

### Classification comparison

| Response | Human reference | Automated |
|---|---|---|
| R1 | 4/40 | 19/40 — Weak |
| R2 | 13/40 | 26/40 — Acceptable with review |
| R3 | 24/40 | 27/40 — Acceptable with review |
| R4 | 33/40 | 32/40 — Strong |
| R5 | 39/40 | 31/40 — Acceptable with review |

The automated evaluator therefore compresses the calibration range substantially: the provisional human range is **4–39**, while the automated range is **19–32**.

## Disagreement analysis

### R1 — major over-scoring

The evaluator gives credit for several dimensions despite the response providing almost no supporting reasoning. The largest issue is the default **3/5 baseline**: a response can omit a criterion and still retain a middle score unless a specific rule detects the omission.

The response also receives Yield/Outcome = 3 even though it does not meaningfully assess an outcome.

**Primary causes:** baseline-score inflation, missing-criterion detection, keyword/length limitations.

### R2 — major over-scoring

The response mentions a qualifying withdrawal, renovation, debt and completion of the renovation, so keyword rules award credit. However, it explicitly recommends withdrawing the full amount without establishing the client's circumstances or assessing the retirement trade-off.

The automated Risk score remains 3 because the current aggressive-recommendation rule does not treat “withdraw the full amount” as an aggressive recommendation for this scenario. Affordability also remains 3 rather than recognising the absence of an affordability assessment.

**Primary causes:** false positive from lexical evidence, missing suitability reasoning, incomplete scenario-specific recommendation detection.

### R3 — moderate disagreement

This response contains useful context and objective considerations, which the evaluator recognises. However, it does not explicitly address risk tolerance/risk capacity, and its affordability score remains below the provisional human reference despite discussing cash reserves and debt.

**Primary causes:** false negatives/limited semantic interpretation and criterion-specific evidence rules.

### R4 — close total, but dimension-level disagreement

The total is close to the provisional reference (32 vs 33), but the dimensions do not align perfectly. Client Context and Objectives are under-scored because the evaluator recognises some terms but does not reliably distinguish comprehensive evidence from partial evidence. Risk is over-scored because the response discusses financial considerations but does not explicitly establish risk tolerance and risk capacity. Clarity and Yield/Outcome are also affected by lexical heuristics.

This is important: a close total does **not** mean the evaluator is calibrated. Dimension-level validity matters.

**Primary causes:** severity error, missing-criterion detection and keyword dependency.

### R5 — major under-scoring

R5 is the strongest response in the provisional human reference, yet the automated evaluator produces 31/40. The most visible issue is Accuracy = 3 despite extensive uncertainty and verification language. The current certainty logic appears to be sensitive to the interaction between risky certainty patterns and safe-uncertainty patterns rather than evaluating the response's overall treatment of uncertainty.

Several other dimensions remain at 4 because the rules generally provide a single keyword-triggered uplift rather than distinguishing strong, comprehensive evidence from merely adequate evidence.

**Primary causes:** severity error, ceiling effects in the rule system, keyword dependency and limited semantic assessment.

## What the baseline demonstrates

The baseline provides evidence for the following methodological problems:

1. **The 3/5 default is too permissive for omission-heavy responses.**
2. **Keyword presence can produce credit without sufficient reasoning.**
3. **The evaluator does not reliably distinguish partial from comprehensive treatment of a criterion.**
4. **Scenario-specific suitability failures are not fully captured.**
5. **Strong responses can be under-scored because the rules do not adequately represent nuanced reasoning.**
6. **Total-score agreement can conceal dimension-level disagreement.**

The calibration therefore supports revisiting the scoring methodology, but it does **not** justify changing individual rules simply to force the five responses to match the provisional reference scores.

## Disagreement taxonomy

For every difference between the human reference and automated result, classify the cause as one or more of:

- **False positive:** automated evaluator gives credit that the response has not earned.
- **False negative:** evaluator misses evidence that supports the criterion.
- **Severity error:** evaluator detects the issue but assigns the wrong severity.
- **Missing criterion:** ground truth requires something not represented in the automated rules.
- **Keyword dependency:** result depends on terminology rather than demonstrated reasoning.
- **Length dependency:** response length changes the score without sufficient evidence of quality.
- **Scenario sensitivity:** the same response behaviour is scored differently depending on scenario-specific facts.

## Initial hypothesis — baseline result

The original hypothesis was:

> Does mentioning a concept produce credit even when the response does not actually reason through that concept?

**SA-001 baseline evidence: yes, in several dimensions.**

R1 and R2 are the clearest examples: the evaluator awards substantial credit despite limited or absent evidence for several ground-truth requirements. Conversely, R5 demonstrates the opposite problem: a response can provide extensive, relevant reasoning and still fail to receive full credit because the rules do not represent that reasoning adequately.

This suggests that the next methodology should evaluate **evidence quality and criterion coverage**, rather than relying primarily on keyword presence and a 3/5 default.

## Acceptance criteria for the next revision

A scoring change should only be made when a disagreement can be traced to an identifiable methodological problem.

The process is:

**ground truth → human reference → automated result → disagreement → cause → scoring change → regression test**

No scoring rule should be added solely to make the automated score match a desired result.

Before changing `accuracy/scoring.py`, the next step is to define a small, explicit evidence rubric for each dimension and test that rubric against R1–R5.

## Validation result

**SA-001 baseline: PASS**

The test harness successfully executed all five calibration responses plus the calibration-set integrity test:

`6 passed in 0.12s`

The baseline evaluator was not modified.

## Next step

Do **not** change `accuracy/scoring.py) yet.

First, convert the disagreement findings above into an explicit **SA-001 evidence rubric** for the eight dimensions. That rubric will define what constitutes 0, 1, 2, 3, 4 and 5 evidence for each dimension. The revised scoring logic can then be designed against the rubric and tested against the frozen R1–R5 calibration set.
