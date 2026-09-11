import pytest
from candidate_payment.aggregations import count_candidates, highest_payment, paid_count
from candidate_payment.core import run99_stream, process_candidate, calculate_eligibility, calculate_payment_amount

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

def test_count_candidates(sample_candidates):
    results = list(run99_stream(sample_candidates))
    assert count_candidates(results) == 2

def test_paid_count(sample_candidates):
    results = list(run99_stream(sample_candidates))
    assert paid_count(results) == 1  # Only John Doe is eligible and has payment

def test_paid_count_with_no_eligible_candidates():
    candidates = [
        {
            "_id": "3",
            "candidateName": "Alice Johnson",
            "candidateId": "C003",
            "isPriorDebt": True,
            "isOnBallot": False,
            "thresholdMet": False,
            "isSon": False,
            "payOverride": False,
            "totalPayment": 2000.0
        }
    ]
    results = list(run99_stream(candidates))
    assert paid_count(results) == 0  # No eligible candidates

def test_paid_count_with_pay_override():
    candidates = [
        {
            "_id": "4",
            "candidateName": "Bob Brown",
            "candidateId": "C004",
            "isPriorDebt": True,
            "isOnBallot": False,
            "thresholdMet": False,
            "isSon": False,
            "payOverride": True,
            "totalPayment": 2500.0
        }
    ]
    results = list(run99_stream(candidates))
    assert paid_count(results) == 1  # Bob Brown is eligible due to pay override

def test_paid_count_with_no_candidates():
    candidates = []
    results = list(run99_stream(candidates))
    assert paid_count(results) == 0  # No candidates at all

def test_paid_count_with_all_ineligible_candidates():
    candidates = [
        {
            "_id": "5",
            "candidateName": "Charlie Davis",
            "candidateId": "C005",
            "isPriorDebt": True,
            "isOnBallot": False,
            "thresholdMet": False,
            "isSon": False,
            "payOverride": False,
            "totalPayment": 3000.0
        },
        {
            "_id": "6",
            "candidateName": "Diana Evans",
            "candidateId": "C006",
            "isPriorDebt": True,
            "isOnBallot": False,
            "thresholdMet": False,
            "isSon": False,
            "payOverride": False,
            "totalPayment": 3500.0
        }
    ]
    results = list(run99_stream(candidates))
    assert paid_count(results) == 0  # All candidates are ineligible

def test_highest_paid_candidate():
    candidates = [
        {
            "_id": "7",
            "candidateName": "Eve Foster",
            "candidateId": "C007",
            "isPriorDebt": False,
            "isOnBallot": True,
            "thresholdMet": True,
            "isSon": True,
            "payOverride": False,
            "totalPayment": 4000.0
        },
        {
            "_id": "8",
            "candidateName": "Frank Green",
            "candidateId": "C008",
            "isPriorDebt": False,
            "isOnBallot": True,
            "thresholdMet": True,
            "isSon": False,
            "payOverride": False,
            "totalPayment": 4500.0
        }
    ]
    results = list(run99_stream(candidates))
    assert highest_payment(results) == 4500.0  # Both Eve Foster and Frank Green are eligible and have payments

def test_highest_paid_candidate_with_no_eligible_candidates():
    candidates = [
        {
            "_id": "9",
            "candidateName": "Grace Hall",
            "candidateId": "C009",
            "isPriorDebt": True,
            "isOnBallot": False,
            "thresholdMet": False,
            "isSon": False,
            "payOverride": False,
            "totalPayment": 5000.0
        }
    ]
    results = list(run99_stream(candidates))
    assert highest_payment(results) == 0  # No eligible candidates, so highest payment is 0