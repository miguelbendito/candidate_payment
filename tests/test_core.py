import pytest
from candidate_payment.aggregations import count_candidates, highest_payment, paid_count
from candidate_payment.core import run99_stream, process_candidate, calculate_eligibility, calculate_payment_amount
from candidate_payment.models import PaymentResult

@pytest.fixture
def sample_candidates():
    return [
        {
            "_id": "1",
            "candidateName": "John Doe",
            "candidateId": "C001",
            "isPriorDebt": False,
            "isOnBallot": True,
            "thresholdMet": True,
            "isSon": True,
            "payOverride": False,
            "totalPayment": 1000.0
        },
        {
            "_id": "2",
            "candidateName": "Jane Smith",
            "candidateId": "C002",
            "isPriorDebt": True,
            "isOnBallot": True,
            "thresholdMet": True,
            "isSon": True,
            "payOverride": False,
            "totalPayment": 1500.0
        }
    ]

def test_run99_stream(sample_candidates):
    results = list(run99_stream(sample_candidates))
    assert len(results) == 2
    assert all(isinstance(r, PaymentResult) for r in results)

def test_process_candidate(sample_candidates):
    candidate = sample_candidates[0]
    result = process_candidate(candidate)
    assert result.candidateId == candidate["candidateId"]
    assert result.isEligible is True
    assert result.paymentAmount == candidate["totalPayment"]

def test_calculate_eligibility(sample_candidates):
    candidate = sample_candidates[0]
    eligible, reason = calculate_eligibility(candidate)
    assert eligible is True
    assert reason is None

    candidate_with_debt = sample_candidates[1]
    eligible, reason = calculate_eligibility(candidate_with_debt)
    assert eligible is False
    assert "The candidate has prior debt" in reason

def test_calculate_payment_amount(sample_candidates):
    candidate = sample_candidates[0]
    amount = calculate_payment_amount(candidate, True)
    assert amount == candidate["totalPayment"]

    amount = calculate_payment_amount(candidate, False)
    assert amount == 0