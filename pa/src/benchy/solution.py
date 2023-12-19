from abc import ABC, abstractmethod


class ISolution(ABC):

    @abstractmethod
    def value(self) -> int | float:
        pass

    def is_better_than(self, other: ISolution) -> bool:
        return self.value() < other.value()
