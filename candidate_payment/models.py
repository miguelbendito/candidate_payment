from dataclasses import dataclass
from typing import Optional

@dataclass
class PaymentResult:
    _id: str
    candidateId: str
    candidateName: str
    isEligible: bool
    paymentAmount: float
    errorCodes: Optional[list] = None
    payOverride: bool = False
    isOnBallot: bool = True
    isSon: bool = True
    isPriorDebt: bool = False
    thresholdMet: bool = True