
from abc import ABC, abstractmethod

class FirewallBackend(ABC):

    @abstractmethod
    def block_ip(self, ip: str) -> None:
        ...

    @abstractmethod
    def unblock_ip(self, ip: str) -> None:
        ...

    @abstractmethod
    def is_blocked(self, ip: str) -> bool:
        ...