# candidate_payment

A small python library that determines eligibility, payment amount and aggregations

## What it does

- Takes a json as an input param.
- Process the json and converts it to a python list of PaymentResult data class
- Core.py processes the json and determines eligibily and payment amount
- Aggregations.py takes the resulted list as the input. The library calculates number of candidates, number of paid candidates, highest payment amount, number of elibible candidates, returns selected fields, returns n number of candidates, returns one candidates given candidate id.

## Usage

```python
import json
from candidate_payment import run99_stream, count_candidates, paid_count, highest_payment

with open("data/cleaned_candidates.json") as f:
    candidates = json.load(f)

results = list(run99_stream(candidates))

print(f"Total processed: {count_candidates(results)}")
print(f"Paid candidates: {paid_count(results)}")
print(f"Highest payment: {highest_payment(results)}")
```

Or run the bundled entrypoint directly:

```bash
uv run python main.py
```

## Installation

Requires Python 3.10+. Dependency management is via [uv](https://github.com/astral-sh/uv).

```bash
uv sync
```

This creates `.venv` and installs the project plus its dev dependencies (pytest) from `uv.lock`.

## Testing

```bash
uv run pytest
```

