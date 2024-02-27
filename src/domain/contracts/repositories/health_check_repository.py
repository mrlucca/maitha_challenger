from abc import ABC, abstractmethod


class IHealthCheckRepository(ABC):
    @abstractmethod
    async def is_available(self): ...
