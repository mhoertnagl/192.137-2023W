from abc import ABC, abstractmethod

from splex import Problem, Solution
from splex.ga import Population


class GA(ABC):

    def __init__(self):
        self._population = Population()

    def run(self, problem: Problem) -> Solution:
        self._population = self.initialize(problem)
        while not self.done():
            selected = self.select(self._population)
            kids = self.recombine(selected)
            kids = self.mutate(kids)
            self._population = self.replace(self._population, kids)
        return self._population.best()

    @abstractmethod
    def initialize(self, problem: Problem):
        pass

    @abstractmethod
    def select(self, population: Population) -> Population:
        pass

    @abstractmethod
    def recombine(self, population: Population) -> Population:
        pass

    @abstractmethod
    def mutate(self, population: Population) -> Population:
        pass

    @abstractmethod
    def replace(self, parents: Population, kids: Population) -> Population:
        pass

    @abstractmethod
    def done(self) -> bool:
        pass
