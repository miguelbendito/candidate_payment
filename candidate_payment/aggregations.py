
from .models import PaymentResult


def count_candidates(results: list[PaymentResult]) -> int:
    return len(results)

def paid_count(results: list[PaymentResult]) -> int:
    return sum(1 for r in results if r.isEligible and r.paymentAmount > 0)

def highest_payment(results: list[PaymentResult]) -> float:
    return max((r.paymentAmount for r in results), default=0)

def first_n(results: list[PaymentResult], n: int = 5) -> list[PaymentResult]:
    return results[:n]

def select_fields(results: list[PaymentResult], fields: list[str]) -> list[dict]:
    return [{k: getattr(r, k) for k in fields if hasattr(r, k)} for r in results]

def get_one_candidate(results: list[PaymentResult], candidateid: str) -> PaymentResult | None:
    for r in results:
        if getattr(r, 'candidateId') == candidateid:
            return r
    return None