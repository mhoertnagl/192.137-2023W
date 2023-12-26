from benchy import *


class Instance:

    def __init__(self, fixture: Fixture, args: dict[str, any]):
        self._fixture = fixture
        self._args = args

    def fixture(self):
        return self._fixture

    def args(self):
        return self._args

    def run(self, problem: IProblem):
        return self._fixture.run(problem, self._args)

    def __repr__(self):
        return self._args.__repr__()

    def __str__(self):
        return self._args.__str__()
