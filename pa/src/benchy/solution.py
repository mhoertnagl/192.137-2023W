from abc import ABC, abstractmethod


class Solution(ABC):

    @abstractmethod
    def value(self) -> int | float:
        pass
