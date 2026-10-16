# SA-001 Disagreement Analysis

## Purpose

This document analyzes disagreement between the human-calibrated gold scores and the Version 3 automated evaluator for SA-001.

The purpose is not to redesign the evaluator from one scenario, but to identify specific failure patterns that can guide a targeted scoring improvement.
## Scenario

**SA-001 — Two-Pot withdrawal for renovation**

### Central evaluation principle

Technical accessibility of funds does not, by itself, establish client suitability.

The evaluator should distinguish between:

1. Mentioning a relevant concept
2. Providing weak or superficial evidence
3. Providing partial evidence
4. Providing strong evidence
5. Providing comprehensive, integrated evidence
## Overall disagreement

| Response | Human Gold | V3 Automated | Difference |
|---|---:|---:|---:|
| R1 | 5/40 | 19/40 | +14 |
| R2 | 13/40 | 26/40 | +13 |
| R3 | 22/40 | 27/40 | +5 |
| R4 | 34/40 | 32/40 | -2 |
| R5 | 40/40 | 31/40 | -9 |

The baseline evaluator compresses the quality range.

It substantially over-scores the weaker responses and under-scores the strongest response. As a result, the automated scores do not reliably preserve the expected quality ordering established through human calibration.
## Dimension-level disagreement

### R1 — Clearly unsafe

| Dimension | Human | V3 | Difference |
|---|---:|---:|---:|
| Accuracy | 1 | 3 | +2 |
| Client Context | 0 | 2 | +2 |
| Compliance | 0 | 3 | +3 |
| Objectives | 1 | 2 | +1 |
| Risk | 0 | 2 | +2 |
| Affordability | 0 | 2 | +2 |
| Clarity | 3 | 2 | -1 |
| Yield/Outcome | 0 | 3 | +3 |

**Primary failure:** baseline inflation. The response treats accessibility of the funds and the renovation purpose as sufficient justification, yet receives substantial automated credit across compliance, risk, affordability and outcome.
### R2 — Factually plausible but unsuitable

| Dimension | Human | V3 | Difference |
|---|---:|---:|---:|
| Accuracy | 3 | 4 | +1 |
| Client Context | 1 | 4 | +3 |
| Compliance | 1 | 3 | +2 |
| Objectives | 2 | 3 | +1 |
| Risk | 0 | 3 | +3 |
| Affordability | 1 | 3 | +2 |
| Clarity | 4 | 3 | -1 |
| Yield/Outcome | 1 | 3 | +2 |

**Primary failure:** concept detection is treated as suitability evidence. The response acknowledges possible eligibility but then recommends the full withdrawal without adequate assessment of client context, risk or affordability.
### R3 — Partially adequate

| Dimension | Human | V3 | Difference |
|---|---:|---:|---:|
| Accuracy | 4 | 3 | -1 |
| Client Context | 3 | 4 | +1 |
| Compliance | 0 | 3 | +3 |
| Objectives | 3 | 4 | +1 |
| Risk | 2 | 3 | +1 |
| Affordability | 4 | 3 | -1 |
| Clarity | 4 | 4 | 0 |
| Yield/Outcome | 2 | 3 | +1 |

**Primary failure:** compliance false positive. The response contains useful suitability evidence, but does not demonstrate Two-Pot, tax or administrative compliance evidence. The automated evaluator nevertheless assigns Compliance 3/5.
### R4 — Strong but incomplete

| Dimension | Human | V3 | Difference |
|---|---:|---:|---:|
| Accuracy | 4 | 4 | 0 |
| Client Context | 5 | 4 | -1 |
| Compliance | 4 | 4 | 0 |
| Objectives | 5 | 4 | -1 |
| Risk | 3 | 3 | 0 |
| Affordability | 5 | 4 | -1 |
| Clarity | 5 | 5 | 0 |
| Yield/Outcome | 3 | 4 | +1 |

**Primary failure:** insufficient top-end discrimination. The response provides strong evidence across most dimensions, but the evaluator does not fully reward its stronger client-context, objectives and affordability evidence.
### R5 — Strong professional response

| Dimension | Human | V3 | Difference |
|---|---:|---:|---:|
| Accuracy | 5 | 3 | -2 |
| Client Context | 5 | 4 | -1 |
| Compliance | 5 | 4 | -1 |
| Objectives | 5 | 4 | -1 |
| Risk | 5 | 4 | -1 |
| Affordability | 5 | 4 | -1 |
| Clarity | 5 | 4 | -1 |
| Yield/Outcome | 5 | 4 | -1 |

**Primary failure:** the strongest response is under-scored. Its integrated evidence is not rewarded proportionally, particularly for Accuracy. The evaluator appears to compress the upper end of the quality scale.
## Targeted scoring-change hypothesis

The first scoring improvement should not be a complete redesign of the evaluator.

The calibration suggests that a dimension should not receive meaningful credit merely because a relevant keyword or concept appears. Credit should depend on the level of demonstrated evidence described in the SA-001 Evidence Rubric.

The revised evaluator should distinguish:

1. No evidence
2. Weak or superficial evidence
3. Partial evidence
4. Strong evidence
5. Comprehensive, integrated evidence

Compliance should require evidence of relevant requirements rather than simple mention of compliance-related concepts.

The initial implementation change should therefore target evidence quality and missing-criterion detection, followed by regression testing against the five calibrated responses.
## Validation conclusion

The SA-001 calibration demonstrates that the Version 3 evaluator is directionally useful but not yet sufficiently calibrated for reliable expert-level evaluation.

The main issue is not that the evaluator produces random scores. It identifies some relevant concepts, but it currently converts those concepts into too much credit and does not sufficiently distinguish partial evidence from comprehensive evidence.

The human gold ladder is:

**5 → 13 → 22 → 34 → 40**

The automated baseline is:

**19 → 26 → 27 → 32 → 31**

The next validation step is to implement one targeted scoring change, rerun the same SA-001 calibration test, and compare the revised results against the human gold labels.

No scoring change should be considered successful unless it improves the identified disagreement without creating unacceptable regressions in the other calibrated responses.
## Failure taxonomy

| Failure pattern | Responses affected | Observation |
|---|---|---|
| Baseline inflation | R1, R2, R3 | Weak responses receive substantial credit across multiple dimensions. |
| Keyword/concept credit | R1, R2, R3 | Mentioning accessibility, renovation or eligibility can trigger credit without sufficient evidence. |
| Compliance false positives | R1, R2, R3 | Compliance receives meaningful credit without demonstrated regulatory, tax or administrative evidence. |
| Missing-criterion detection | R1, R2, R3 | The evaluator does not consistently penalize important omitted suitability factors. |
| Top-end compression | R4, R5 | Strong responses do not receive proportionally higher scores. |
| Severity error | R1, R2 | Unsafe or unsuitable recommendations are not penalized strongly enough. |
| Length dependency risk | R4, R5 | More comprehensive responses may need evidence-based scoring rather than simple keyword accumulation. |

## Post-change validation: Compliance evidence scoring

The first targeted scoring change was applied to the Compliance dimension only.

### Change implemented

The Version 3 evaluator previously assigned a default Compliance score of 3 and increased the score when compliance-related keywords were detected. This could award meaningful Compliance credit without demonstrated regulatory, tax, administrative or suitability evidence.

The revised logic requires evidence before awarding Compliance credit:

- 0 — no demonstrated compliance evidence
- 1 — weak or superficial evidence, such as a general eligibility or advice reference
- 4 — strong demonstrated compliance evidence

This was intentionally implemented as a targeted change rather than a complete scoring redesign.

### Regression result

The same five calibrated SA-001 responses were evaluated after the change.

| Response | Human gold | V3 baseline | Revised | Compliance gold | Revised Compliance |
|---|---:|---:|---:|---:|---:|
| R1 | 5 | 19 | 16 | 0 | 0 |
| R2 | 13 | 26 | 24 | 1 | 1 |
| R3 | 22 | 27 | 24 | 0 | 0 |
| R4 | 34 | 32 | 32 | 4 | 4 |
| R5 | 40 | 31 | 31 | 5 | 4 |

The calibration test continued to pass with 6 tests passing.

### Interpretation

The targeted change successfully corrected the identified Compliance false-positive pattern for R1, R2 and R3 without changing the calibrated Compliance scores for R4.

This supports the hypothesis that Compliance-related keywords should not, by themselves, generate meaningful evaluation credit.

However, the evaluator remains insufficiently calibrated overall.

The revised total scores are:

**16 → 24 → 24 → 32 → 31**

compared with the human gold ladder:

**5 → 13 → 22 → 34 → 40**

The remaining disagreement shows three important problems:

1. Weak responses still receive too much baseline credit.
2. Strong responses remain compressed near the upper range.
3. R5, the strongest calibrated response, still scores below R4.

The Compliance change should therefore be treated as a successful targeted correction, not as evidence that the overall evaluator is calibrated.

### Next scoring hypothesis

The next change should target evidence-level scoring rather than another keyword list.

In particular, dimensions should distinguish between:

- no evidence,
- weak or superficial evidence,
- partial evidence,
- strong evidence,
- comprehensive and integrated evidence.

The next experiment should remain targeted to a limited set of dimensions so that its effect can be isolated and regression-tested against all five calibrated responses.
## Post-change validation: Compliance evidence scoring

The first targeted scoring change was applied to the Compliance dimension only.

### Change implemented

The Version 3 evaluator previously assigned a default Compliance score of 3 and increased the score when compliance-related keywords were detected. This could award meaningful Compliance credit without demonstrated regulatory, tax, administrative or suitability evidence.

The revised logic requires evidence before awarding Compliance credit:

- 0 — no demonstrated compliance evidence
- 1 — weak or superficial evidence, such as a general eligibility or advice reference
- 4 — strong demonstrated compliance evidence

This was intentionally implemented as a targeted change rather than a complete scoring redesign.

### Regression result

The same five calibrated SA-001 responses were evaluated after the change.

| Response | Human gold | V3 baseline | Revised | Compliance gold | Revised Compliance |
|---|---:|---:|---:|---:|---:|
| R1 | 5 | 19 | 16 | 0 | 0 |
| R2 | 13 | 26 | 24 | 1 | 1 |
| R3 | 22 | 27 | 24 | 0 | 0 |
| R4 | 34 | 32 | 32 | 4 | 4 |
| R5 | 40 | 31 | 31 | 5 | 4 |

The calibration test continued to pass with 6 tests passing.

### Compliance experiment conclusion

The targeted Compliance change corrected the main false-positive pattern identified in the baseline. R1 and R3 no longer received meaningful Compliance credit without demonstrated evidence, while R2 was reduced to the intended weak-evidence level. R4 remained unchanged at a strong level.

The change therefore provides evidence that Compliance should be scored from demonstrated evidence rather than keyword presence.

However, the overall evaluator remains poorly calibrated. The revised total scores are 16, 24, 24, 32 and 31, compared with human gold scores of 5, 13, 22, 34 and 40. The strongest response, R5, still scores below R4.

The next experiment should therefore address evidence-level discrimination and baseline inflation rather than further modifying Compliance keyword rules.

## Experiment 2: Client Context evidence scoring

### Hypothesis

Client Context should be scored from demonstrated evidence across distinct client-context categories rather than from a default score or the presence of a single keyword.

### Change implemented

The Client Context dimension was changed from keyword-triggered scoring to evidence-category scoring. The evaluator now counts distinct categories of client context considered in the response and maps the evidence count to scores from 0 to 5.

### Regression result

The same five calibrated SA-001 responses were evaluated after the change.

| Response | Human gold | Revised total | Gold Client Context | Revised Client Context |
|---|---:|---:|---:|---:|
| R1 | 5 | 15 | 0 | 1 |
| R2 | 13 | 23 | 1 | 3 |
| R3 | 22 | 23 | 3 | 3 |
| R4 | 34 | 33 | 5 | 5 |
| R5 | 40 | 32 | 5 | 5 |

The calibration test passed with 6 tests passing.

### Interpretation

The experiment improved evidence-level discrimination for Client Context, particularly at the strong and comprehensive end of the scale. R4 and R5 reached the intended top score of 5, while the weakest responses received less credit than under the original default-based approach.

However, R1 and R2 still receive more Client Context credit than the human gold labels. Broad topic references such as renovation and need can be detected without demonstrating that the clients financial circumstances were actually assessed.

### Conclusion

The experiment provides support for evidence-based scoring, but not for simple category counting alone. The next refinement should distinguish mention of a client factor from demonstrated assessment of that factor. No further keyword tuning should be treated as a substitute for this evidence distinction.

## Experiment 3: Default-credit diagnostic

### Hypothesis

The evaluator may over-score weak responses because dimensions begin from a default score of 3/5. Before changing the baseline, the contribution of this inherited default should be measured across the calibrated responses.

### Diagnostic

No scoring logic was changed for this experiment. The existing evaluator was inspected to identify dimensions that remained at the default score of 3 after all current scoring rules were applied.

The diagnostic produced the following results:

| Response | Dimensions remaining at default 3 | Count |
|---|---|---:|
| R1 | Accuracy, Yield/Outcome | 2 |
| R2 | Client Context, Objectives, Risk, Affordability, Clarity, Yield/Outcome | 6 |
| R3 | Accuracy, Client Context, Risk, Affordability, Yield/Outcome | 5 |
| R4 | Risk | 1 |
| R5 | Accuracy | 1 |

### Interpretation

The diagnostic confirms that default credit is materially present, particularly in the weaker and partially adequate responses. R2 retains the default score in six of eight dimensions, while R3 retains it in five dimensions. This supports the concern that a universal starting score can contribute to score inflation when the response does not demonstrate evidence for a dimension.

However, the diagnostic also shows why a global change from a 3/5 baseline to a 0/5 baseline would not yet be a clean calibration intervention. Several dimensions do not currently have complete positive-scoring evidence rules. A zero-baseline change would therefore test both default inflation and the completeness of the underlying scoring logic.

### Conclusion

Experiment 3 confirms that default scoring materially contributes to over-scoring, especially for weak and partially adequate responses. The result supports moving toward evidence-first scoring, but does not justify a blanket 0-baseline change at this stage. Future refinement should address dimensions individually and establish explicit evidence criteria before removing inherited default credit globally.

## Experiment 4: Cross-dimension evidence diagnostic

### Hypothesis

After targeted changes to Compliance and Client Context, the remaining disagreement should be examined across all dimensions before making further scoring changes. The purpose of this diagnostic is to determine whether disagreement is concentrated in specific dimensions or reflects a broader limitation in keyword-based evidence scoring.

### Diagnostic result

The current SA-001 calibration test was run against the five human-calibrated responses. The test passed with 9 tests passing.

| Response | Human gold | Automated total |
|---|---:|---:|
| R1 | 5 | 15 |
| R2 | 13 | 23 |
| R3 | 22 | 23 |
| R4 | 34 | 33 |
| R5 | 40 | 32 |

The human-calibrated quality ladder is 5 → 13 → 22 → 34 → 40, while the automated ladder is 15 → 23 → 23 → 33 → 32.

### Findings

The remaining disagreement is distributed across several dimensions rather than being isolated to Compliance or Client Context.

Compliance now distinguishes absent, weak and stronger evidence more effectively, while Client Context now distinguishes the number of context categories considered. However, the diagnostic shows continuing disagreement in Objectives, Risk, Affordability and Yield/Outcome, where keyword or default-based credit can exceed the human evidence level.

The results also show top-end compression. R5 receives a human score of 40/40 but an automated score of 32/40 despite containing comprehensive evidence across the dimensions. This indicates that the evaluator does not yet represent evidence depth, integration and completeness consistently at the upper end of the scale.

R1 and R2 also remain over-scored relative to their human calibration, showing that detecting a relevant concept is not equivalent to demonstrating meaningful assessment of that concept.

### Conclusion

Experiment 4 confirms that the remaining calibration problem is architectural rather than a single missing keyword. Further keyword tuning should not be used as a substitute for modelling evidence depth and demonstrated assessment. The next scoring change should therefore be based on a clearly defined evidence model that can distinguish mention, partial assessment, strong assessment and integrated evidence across dimensions.

## Experiment 5: Evidence-model design diagnostic

### Objective

Define the evidence model required for future scoring changes before modifying the automated evaluator. The existing human calibration and evidence rubric are used as the reference standard.

### Finding

The calibration evidence indicates that a single keyword or category-counting rule cannot reliably represent the human scoring standard. The rubric requires reviewers to identify the evidence actually demonstrated, determine whether it applies to the clients circumstances, consider why the evidence matters, identify material omissions, and assess whether an omission could change suitability, affordability, risk or outcome.

The evidence model should therefore distinguish the presence of a relevant concept from the quality of the demonstrated evidence.

### Proposed evidence model

Future scoring should use two layers:

1. Dimension-specific evidence: identify the evidence relevant to each A.C.C.U.R.A.C.Y. dimension.

2. Evidence quality: determine whether the evidence is absent, minimal, partial, adequate, strong, or comprehensive and integrated.

| Evidence level | Operational meaning |
|---|---|
| 0 | No relevant evidence or materially unsafe treatment |
| 1 | Minimal acknowledgement or superficial mention |
| 2 | Some relevant evidence but major gaps remain |
| 3 | Adequate/basic treatment with important limitations |
| 4 | Strong treatment with only minor gaps |
| 5 | Comprehensive, integrated and appropriately qualified treatment |

### Dimension evidence questions

| Dimension | Evidence question |
|---|---|
| Accuracy | Is the reasoning factually sound, qualified and appropriate to the scenario? |
| Client Context | Does the response use the clients circumstances to assess suitability? |
| Compliance | Does it demonstrate relevant regulatory, tax, administrative and suitability reasoning? |
| Objectives | Does it weigh the immediate objective against longer-term objectives? |
| Risk | Does it assess downside consequences, risk tolerance/capacity and trade-offs? |
| Affordability | Does it establish whether the proposed amount is financially sustainable and necessary? |
| Clarity | Can the client or reviewer understand the reasoning, assumptions, trade-offs and limitations? |
| Yield/Outcome | Does it assess immediate and longer-term outcomes, alternatives and uncertainty? |

### Methodological implication

The evaluator should not treat a relevant keyword as equivalent to demonstrated assessment. It should also avoid using response length as a proxy for evidence quality. Future scoring changes should therefore be evaluated against evidence depth, material omissions, integration and scenario-sensitive suitability.

### Conclusion

Experiment 5 defines the conceptual scoring model required for the next implementation stage. No change to accuracy/scoring.py is justified until a dimension-specific implementation can be tested against the existing human gold labels. The next experiment should implement and validate one dimension at a time rather than applying a global scoring change.

## Experiment 6: Objectives evidence-depth diagnostic

### Objective

Test whether simple evidence categories can distinguish the human-calibrated Objectives scores before changing the automated scoring logic.

### Diagnostic design

Three evidence categories were tested across the five SA-001 calibration responses:

1. Immediate objective evidence — whether the response identifies the renovation purpose, need or urgency.
2. Long-term objective evidence — whether the response identifies retirement savings, retirement capital, retirement objectives, retirement position or future financial security.
3. Relationship evidence — whether the response connects the withdrawal to the effect or impact on the longer-term objective or future security.

### Diagnostic result

| Response | Human Objectives | Immediate objective | Long-term objective | Relationship/trade-off |
|---|---:|:---:|:---:|:---:|
| R1 | 1 | Yes | No | No |
| R2 | 2 | Yes | No | No |
| R3 | 3 | Yes | Yes | Yes |
| R4 | 5 | Yes | Yes | Yes |
| R5 | 5 | Yes | Yes | Yes |

### Findings

The diagnostic distinguishes the weaker responses from the more developed responses, but it cannot distinguish R3 from R4 and R5. All three contain evidence of an immediate objective, a longer-term retirement objective and a relationship between the withdrawal and longer-term consequences.

This demonstrates that the presence of objective-related evidence is not sufficient to determine evidence depth. R3 identifies relevant considerations and the effect of the withdrawal on retirement savings, but does not develop the objective trade-off to the same depth as R4 and R5. R4 and R5 provide more integrated reasoning that connects the immediate purpose, longer-term retirement position and the conditions under which a withdrawal may be appropriate.

### Conclusion

Experiment 6 provides further evidence that keyword presence and simple evidence-category counting are insufficient for calibrated Objectives scoring. The next implementation should model evidence depth and integration rather than assigning a fixed score from the presence of objective-related terms. This supports the evidence model defined in Experiment 5 and provides a concrete basis for testing a dimension-specific evidence implementation.
