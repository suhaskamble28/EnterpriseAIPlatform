from abc import ABC, abstractmethod

from models.evidence import NormalizedEvidence


class EvidenceProvider(ABC):

    @abstractmethod
    def search_transaction(
        self,
        transaction_id: str
    ) -> NormalizedEvidence:
        pass