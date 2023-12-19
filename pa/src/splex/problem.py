from abc import ABC

from benchy import Problem


class SPlexProblem(Problem, ABC):

    def __init__(self, name: str):
        self._name = name

    def name(self):
        return self._name
