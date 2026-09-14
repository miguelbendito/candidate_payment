"""Export PaymentResult data to CSV files.

Only a subset of PaymentResult is written out: candidateId, candidateName,
isEligible, paymentAmount, and errorCodes.

The writer is implemented as a custom context manager (via @contextmanager)
so the file can be opened once, written to row-by-row as results stream in
from run99_stream, and guaranteed to close even if the caller's `with`
block raises partway through.
"""

import csv
from contextlib import contextmanager
from pathlib import Path
from typing import Iterable, Iterator

from .models import PaymentResult

FIELDNAMES = ["candidateId", "candidateName", "isEligible", "paymentAmount", "errorCodes"]


def _to_row(result: PaymentResult) -> dict:
    """Pull just FIELDNAMES out of a PaymentResult as a plain dict."""

    return {
        "candidateId": result.candidateId,
        "candidateName": result.candidateName,
        "isEligible": result.isEligible,
        "paymentAmount": result.paymentAmount,
        "errorCodes": ",".join(result.errorCodes or [])
    }


@contextmanager
def csv_results_writer(filepath: str | Path) -> Iterator[csv.DictWriter]:
    """Context manager that opens `filepath` for CSV writing."""
    
    with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=FIELDNAMES)
        writer.writeheader()
        yield writer


def export_to_csv(results: Iterable[PaymentResult], filepath: str | Path) -> None:

    with csv_results_writer(filepath) as writer:
        for result in results:
            writer.writerow(_to_row(result))


