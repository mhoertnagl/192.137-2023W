from abc import ABC, abstractmethod

from benchy import Problem, Solution


class Fixture(ABC):

    @abstractmethod
    def run(self, problem: Problem, args: dict[str, any]) -> Solution:
        pass
