import requests
from services.evidence_provider import EvidenceProvider

from models.evidence import (
    NormalizedEvidence,
    FailureEvidence,
    TechnicalEvidence
)


class SplunkService(EvidenceProvider):

    def __init__(self):
        self.base_url = "https://localhost:8089"
        self.username = "admin"
        self.password = "ResolveAI@2026!"

    def search_transaction(self, transaction_id: str) -> NormalizedEvidence:

        search = (
            'search index=resolveai '
            f'transaction_id="{transaction_id}" '
            '| table transaction_id trace_id business_domain '
            'business_operation business_channel service '
            'business_outcome failure_category failure_type '
            'dependency_name dependency_type level message'
        )

        response = requests.post(
            f"{self.base_url}/services/search/jobs",
            auth=(self.username, self.password),
            data={
                "output_mode": "json",
                "exec_mode": "oneshot",
                "search": search
            },
            verify=False,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        results = data.get("results", [])

        if not results:
            raise ValueError(
                f"No Splunk evidence found for transaction {transaction_id}"
            )

        result = results[0]

        return NormalizedEvidence(
            transaction_id=result.get("transaction_id", transaction_id),

            business_domain=result.get("business_domain"),
            business_operation=result.get("business_operation"),
            business_channel=result.get("business_channel"),
            business_outcome=result.get("business_outcome"),

            failure=FailureEvidence(
                category=result.get("failure_category"),
                type=result.get("failure_type"),
                dependency=result.get("dependency_name"),
                dependency_type=result.get("dependency_type")
            ),

            technical=TechnicalEvidence(
                trace_id=result.get("trace_id"),
                service=result.get("service"),
                level=result.get("level"),
                message=result.get("message")
            ),

            source="Splunk"
        )