from benchy import Fixture


class Harness:

    def __init__(self):
        self._repetitions = 1
        self._parameters: dict[str, list] = dict()
        self._fixtures: list[Fixture] = list()

    def set_repetitions(self, repetitions: int):
        self._repetitions = repetitions
        return self

    def add_parameter(self, name: str, values: list[any]):
        self._parameters[name] = values
        return self

    def add_fixture(self, fixture: Fixture):
        self._fixtures.append(fixture)
        return self

    # def __iter__(self):

