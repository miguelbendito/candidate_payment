from typing import Iterator
from .models import PaymentResult

def run99_stream(candidates: list[dict]) -> Iterator[PaymentResult]:
    for row in candidates:
        yield process_candidate(row)  # your calc function from before


def process_candidate(row: dict) -> PaymentResult:
    eligible, reason = calculate_eligibility(row)
    amount = calculate_payment_amount(row,eligible)
    return PaymentResult(_id=row.get('_id'),
                         isEligible=eligible,
                         paymentAmount=amount,
                         candidateName=row.get('candidateName'),
                         candidateId = row.get('candidateId'),
                         isPriorDebt = row.get('isPriorDebt', False),
                         isOnBallot = row.get('isOnBallot', True),
                         isSon = row.get('isSon', True),
                         thresholdMet = row.get('thresholdMet', True),
                         payOverride = row.get('payOverride', False),
                         errorCodes=reason if reason else None)

def calculate_eligibility(row: dict) -> tuple[bool, list[str] | None]:
    errorCodes = []
    isEligible = True

    if row.get('isPriorDebt', False) == True:
        isEligible = False
        errorCodes.append('The candidate has prior debt')

    if not row.get('isOnBallot', True):
        isEligible = False
        errorCodes.append('The candidate is not on the ballot')  

    if not row.get('thresholdMet', True):
            isEligible = False
            errorCodes.append('The candidate did not meet the minimum threshold to receive payment')

    if not row.get('isSon', True):
        errorCodes.append('The candidate does not have a valid statement of need')

    if isEligible == False and row.get('payOverride', False) == True:
        isEligible = True
        errorCodes.append('The candidate has a pay override')

    return isEligible, errorCodes if errorCodes else None


def calculate_payment_amount(row: dict, eligible: bool) -> float:
    if not eligible:
        return 0
    return row.get('totalPayment', 0)  # default to 0 if not present
