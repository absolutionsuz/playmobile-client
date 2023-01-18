from abc import ABC, abstractmethod
from typing import Iterable, Optional

from playmobile.entities import SMS, Timing


class ClientInterface(ABC):
    """Interface for Playmobile client."""

    @abstractmethod
    def send_sms(self, sms: SMS, *, timing: Optional[Timing] = None) -> None:
        """Send single SMS to Playmobile."""

    @abstractmethod
    def send_sms_batch(
        self,
        sms_batch: Iterable[SMS],
        *,
        timing: Optional[Timing] = None,
    ) -> None:
        """Send batch of SMS to Playmobile."""
