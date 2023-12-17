from benchy import *


class Instance:

    def __init__(self, fixture: Fixture, args: dict[str, any]):
        self._fixture = fixture
        self._args = args

    def fixture(self):
        return self._fixture

    def args(self):
        return self._args

    def run(self, problem: Problem):
        self._fixture.run(problem, self._args)
