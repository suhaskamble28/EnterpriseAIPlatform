from pydantic import BaseModel
from typing import Optional


class FailureEvidence(BaseModel):
    category: Optional[str] = None
    type: Optional[str] = None
    dependency: Optional[str] = None
    dependency_type: Optional[str] = None


class TechnicalEvidence(BaseModel):
    trace_id: Optional[str] = None
    service: Optional[str] = None
    level: Optional[str] = None
    message: Optional[str] = None


class NormalizedEvidence(BaseModel):
    transaction_id: str
    business_domain: Optional[str] = None
    business_operation: Optional[str] = None
    business_channel: Optional[str] = None
    business_outcome: Optional[str] = None

    failure: FailureEvidence
    technical: TechnicalEvidence

    source: str