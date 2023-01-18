from abc import ABC, abstractmethod
from typing import Optional

from playmobile.entities import SMS, Timing


class ClientInterface(ABC):
    """Interface for Playmobile client."""

    @abstractmethod
    def send_sms(self, sms: SMS, *, timing: Optional[Timing] = None) -> None:
        """Send single SMS to Playmobile."""
