from abc import ABC, abstractmethod


class ISolution(ABC):

    @abstractmethod
    def value(self) -> int | float:
        pass

    def is_better_than(self, other) -> bool:
        return self.value() < other.value()

    @abstractmethod
    def is_feasible(self):
        pass


def best_of(candidates: list[ISolution]) -> ISolution | None:
    winner: ISolution | None = None
    for candidate in candidates:
        if candidate.is_better_than(winner):
            winner = candidate
    return winner
