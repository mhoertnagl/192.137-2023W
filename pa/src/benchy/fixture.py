from abc import ABC, abstractmethod

from benchy import IProblem, ISolution


class Fixture(ABC):

    @abstractmethod
    def run(self, problem: IProblem, args: dict[str, any]) -> ISolution:
        pass
