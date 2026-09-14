import pytest

from candidate_payment import run99_stream, count_candidates, highest_payment, select_fields, get_one_candidate, paid_count, first_n
from candidate_payment.export import export_to_csv


def test_export_to_csv(tmp_path):
    candidates = [
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

    results = list(run99_stream(candidates))
    output_file = tmp_path / "payment_results.csv"
    export_to_csv(results, output_file)

    # Read the CSV back and check its contents
    with open(output_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    assert lines[0].strip() == 'candidateId,candidateName,isEligible,paymentAmount,errorCodes'
    assert 'C001' in lines[1]
    assert 'C002' in lines[2]