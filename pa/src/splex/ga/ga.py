from abc import ABC, abstractmethod

from splex import Problem, Solution
from splex.con import Construction
from splex.ga.population import Population
from splex.ga.comb import Combiner
from splex.ga.mut import Mutator
from splex.ga.rep import Replacer
from splex.ga.sel import Selection


# Population size as a parameter.

# Recombine
# - Component based
#   - Wir wollen Komponenten die in beiden Elternteilen vorkommen erhalten.
#   - Wir wollen möglichst viele Komponenten erhalten.
# - Edge based
#   - A bit for each edge
#   - classical uniform crossover
#   - Repair function

# Mutate
# - 2 exchange
# - Component Merge

# Replace
# - Roulette replace

class GA:
    def __init__(self,
                 size: int,
                 construction: Construction,
                 selection: Selection,
                 combiner: Combiner,
                 mutator: Mutator,
                 replacer: Replacer):
        self._size = size
        self._construction = construction
        self._selection = selection
        self._combiner = combiner
        self._mutator = mutator
        self._replacer = replacer
        self._population = Population()
        self._best_values: list[int | float] = []  # History of best values
        self._best: Solution | None = None         # Best solution

    def best_values(self):
        return self._best_values

    def run(self, problem: Problem) -> Solution:
        self._initialize(problem)
        while not self.done(problem, self._population):
            selected = self._select(problem)
            kids = self._combiner.recombine(problem, selected)
            self._mutate(problem, kids)
            self._replace(problem, kids)
            self._update_best()
        return self._best

    def _initialize(self, problem: Problem):
        solutions = self._construction.construct_many(problem, self._size)
        # solutions = []
        # for _ in range(self._size):
        #     solution = self._construction.construct(problem)
        #     solutions.append(solution)
        self._population = Population(solutions)

    def _select(self, problem: Problem) -> Population:
        return self._selection.select(problem, self._population)

    def _mutate(self, problem: Problem, population: Population):
        # TODO: mutate only part of the population?
        for solution in population:
            self._mutator.mutate(problem, solution)

    def _replace(self, problem: Problem, kids: Population):
        self._population = self._replacer.replace(
            problem,
            self._population,
            kids,
            self._size
        )

    def _update_best(self):
        best = self._population.best()
        self._best_values.append(best.value())
        if self._best is None or best.is_better_than(self._best):
            self._best = best

# class GA(ABC):
#
#     def __init__(self):
#         self._population = Population()
#
#     def run(self, problem: Problem) -> Solution:
#         self._population = self.initialize(problem)
#         while not self.done(problem, self._population):
#             selected = self.select(problem, self._population)
#             kids = self.recombine(problem, selected)
#             kids = self.mutate(problem, kids)
#             self._population = self.replace(problem, self._population, kids)
#         return self._population.best()
#
#     @abstractmethod
#     def initialize(self, problem: Problem, size: int) -> Population:
#         pass
#
#     @abstractmethod
#     def select(self,
#                problem: Problem,
#                population: Population) -> Population:
#         pass
#
#     @abstractmethod
#     def recombine(self,
#                   problem: Problem,
#                   population: Population) -> Population:
#         pass
#
#     @abstractmethod
#     def mutate(self,
#                problem: Problem,
#                population: Population) -> Population:
#         pass
#
#     @abstractmethod
#     def replace(self,
#                 problem: Problem,
#                 parents: Population,
#                 kids: Population) -> Population:
#         pass
#
#     @abstractmethod
#     def done(self,
#              problem: Problem,
#              population: Population) -> bool:
#         pass
