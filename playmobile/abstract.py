from abc import ABC, abstractmethod

from playmobile.entities import SMS


class ClientInterface(ABC):
    """Interface for Playmobile client."""

    @abstractmethod
    def send_sms(self, sms: SMS) -> None:
        """Send SMS to Playmobile."""
