# SA-001 Calibration Validation

## Status

**Validation phase:** Baseline calibration  
**Scenario:** SA-001 — Two-Pot withdrawal for renovation  
**Evaluator baseline:** `accuracy/scoring.py` Version 3  
**Automated results:** Pending execution in the repository test environment  
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

## Automated evaluation

The current `evaluate_response()` implementation is deliberately retained unchanged for this baseline experiment.

For each response, record:

- eight automated dimension scores;
- total score;
- percentage;
- classification;
- critical flags.

Do not alter the evaluator before recording the baseline.

## Disagreement taxonomy

For every difference between the human reference and automated result, classify the cause as one or more of:

- **False positive:** automated evaluator gives credit that the response has not earned.
- **False negative:** evaluator misses evidence that supports the criterion.
- **Severity error:** evaluator detects the issue but assigns the wrong severity.
- **Missing criterion:** ground truth requires something not represented in the automated rules.
- **Keyword dependency:** result depends on terminology rather than demonstrated reasoning.
- **Length dependency:** response length changes the score without sufficient evidence of quality.
- **Scenario sensitivity:** the same response behaviour is scored differently depending on scenario-specific facts.

## Initial hypothesis to test

The current evaluator starts all dimensions at **3/5** and then adjusts scores using lexical triggers, response length and selected scenario-response interactions.

This creates a validity question:

> Does mentioning a concept produce credit even when the response does not actually reason through that concept?

The calibration set is designed to test this directly.

## Acceptance criteria for the next revision

A scoring change should only be made when a disagreement can be traced to an identifiable methodological problem.

The process is:

**ground truth → human reference → automated result → disagreement → cause → scoring change → regression test**

No scoring rule should be added solely to make the automated score match a desired result.

## Next step

Run R1–R5 through the exact current evaluator and record the results in this document. Then compare the automated output with the provisional expert reference before changing `accuracy/scoring.py`.

