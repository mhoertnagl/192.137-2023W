from itertools import product

from benchy import Fixture


class Harness:

    def __init__(self):
        self._parameters: dict[str, list] = dict()
        self._fixtures: list[Fixture] = list()

    def add_parameter(self, name: str, values: list[any]):
        self._parameters[name] = values
        return self

    def add_fixture(self, fixture: Fixture):
        self._fixtures.append(fixture)
        return self

    def __iter__(self):
        parameters = self._parameters.values()
        for parameter in parameters:
            yield parameter
        # product()

