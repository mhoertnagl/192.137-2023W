from itertools import product

from benchy import *


class Harness:

    def __init__(self, repetitions: int = 10):
        self._repetitions = repetitions
        self._parameters: dict[str, list] = dict()
        self._fixture: Fixture | None = None

    def add_parameter(self, name: str, values: list[any]):
        self._parameters[name] = values
        return self

    def set_fixture(self, fixture: Fixture):
        self._fixture = fixture
        return self

    def repetitions(self) -> int:
        return self._repetitions

    def fixture(self) -> Fixture:
        return self._fixture

    def __iter__(self) -> list[Instance]:
        # TODO: Return FixtureRunners
        parameters = self._parameters.values()
        for parameter in parameters:
            yield parameter
        # product()

