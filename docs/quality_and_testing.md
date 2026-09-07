# Quality and Testing

The A.C.C.U.R.A.C.Y. framework uses automated tests and continuous integration to help ensure that evaluation logic remains reliable as the project evolves.

## Current test status

The current test suite contains:

- **11 automated tests**
- **11 tests passing**
- **0 failing tests**
- Automated execution through **GitHub Actions**

The test suite is designed to provide regression protection for the evaluation engine and its safety-related behaviour.

## What is tested

The tests cover important evaluation behaviours including:

### Evaluation scoring

The framework can evaluate AI-generated financial responses across the eight A.C.C.U.R.A.C.Y. dimensions:

- Accuracy
- Client Context
- Compliance
- Objectives
- Risk
- Affordability
- Clarity
- Yield / Outcome

Each dimension is scored from 0–5, producing a maximum raw score of 40.

### Safety regression testing

Dedicated safety cases test the evaluator's ability to identify potentially unsafe financial responses.

Examples include:

- Unsupported investment guarantees
- Excessive certainty about investment outcomes
- Risk and suitability concerns
- Affordability concerns
- Liquidity considerations
- Missing material client context

### Uncertainty detection

The evaluator distinguishes between potentially excessive certainty and appropriately qualified financial language.

For example:

**Higher-risk language:**

> “This investment is guaranteed to provide strong returns.”

versus:

**More appropriate uncertainty:**

> “Investment returns are uncertain and depend on the client's circumstances and market conditions.”

This helps reduce false confidence in AI-generated financial responses.

## Continuous integration

The repository uses **GitHub Actions** to automatically run the test suite when changes are pushed.

The CI workflow helps ensure that changes to the evaluation engine do not unintentionally break existing behaviour.

The workflow currently runs the project's automated tests using Python 3.12.

## Why automated testing matters

An AI evaluation framework should itself be evaluated.

If the scoring logic changes without regression testing, a previously detected safety issue could accidentally stop being detected.

Automated regression tests therefore provide an additional quality-control layer:

**Code change → Automated tests → Pass / fail signal → Human review**

This supports a human-in-the-loop approach to financial AI evaluation.

## Current limitations

The current test suite is intentionally focused on core framework behaviour and representative safety cases.

Passing tests do **not** prove that every possible financial-advice response is safe or correct.

Financial regulation, tax rules, product information and other jurisdiction-specific requirements can change and should be independently verified when the framework is used for real-world evaluation.

## Quality principle

> **A reliable AI evaluation system must test its own evaluation logic.**

The purpose of the test suite is therefore not to claim that the framework is perfect, but to provide a transparent and repeatable mechanism for detecting regressions as the framework develops.
