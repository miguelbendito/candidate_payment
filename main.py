import json
from pathlib import Path
from contextlib import contextmanager
from candidate_payment import run99_stream, count_candidates, highest_payment, select_fields, get_one_candidate, paid_count, first_n

def load_candidates(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)

def main():
    data_path = Path(__file__).parent / 'data' / 'cleaned_candidates.json'
    candidates = load_candidates(data_path)

    results = list(run99_stream(candidates))

    print(f"Total processed: {count_candidates(results)}")
    print(f"Paid candidates: {paid_count(results)}")
    print(f"Highest payment: {highest_payment(results)}")
    print("Sample output:")
    print(select_fields(first_n(results, 5), ['candidateId', 'paymentAmount', 'isEligible', 'errorCodes']))

if __name__ == '__main__':
    main()