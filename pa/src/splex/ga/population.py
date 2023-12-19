from splex import Solution


class Population(list[Solution]):

    def best(self) -> Solution:
        best: Solution | None = None
        for individual in self:
            if best is None or individual.is_better_than(best):
                best = individual
        return best