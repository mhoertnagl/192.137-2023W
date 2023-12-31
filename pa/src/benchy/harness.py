from .fixture import Fixture
from .instance import Instance

# TODO: Domain is actually a set.


class Harness:

    def __init__(self, name: str, fixture: Fixture, repetitions: int = 10):
        self._name = name
        self._repetitions = repetitions
        self._parameters: dict[str, list] = dict()
        self._fixture = fixture

    def add_parameter(self, name: str, values: list[any]):
        self._parameters[name] = values
        return self

    def name(self):
        return self._name

    def repetitions(self):
        return self._repetitions

    def parameter_names(self):
        return list(self._parameters.keys())

    def domains(self):
        return list(self._parameters.items())

    def size(self):
        sz = 1
        for values in self._parameters.values():
            sz *= len(values)
        return sz * self._repetitions

    def __iter__(self):
        return self._generate_instances(self.domains(), {})

    def _generate_instances(self,
                           domains: list[(str, list)],
                           args: dict[str, any]):
        if len(args) >= len(domains):
            yield Instance(self._fixture, args)
        else:
            name, domain = domains[len(args)]
            for element in domain:
                args1 = args.copy()
                args1[name] = element
                yield from self._generate_instances(domains, args1)
