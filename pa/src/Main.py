#!/usr/bin/env python3
# -*- coding: utf8 -*-

from itertools import product

# n = 3
# start_solution = [False] * n
# start_clauses: list[list[int]] = [[]]


def one_flip(solution: list[bool]) -> list[list[bool]]:
    flipped = []
    for i in range(len(solution)):
        flip = solution.copy()
        flip[i] = not flip[i]
        flipped.append(flip)
    return flipped


def evaluate(clauses: list[list[int]], solution: list[bool]):
    value = True
    for clause in clauses:
        clause_value = False
        for literal in clause:
            if literal > 0:
                clause_value = clause_value or solution[literal-1]
            if literal < 0:
                clause_value = clause_value or not solution[abs((literal+1))]
        value = value and clause_value
    return value


def clauses_fulfilled(clauses: list[list[int]], solution: list[bool]):
    count = 0
    for clause in clauses:
        for literal in clause:
            if literal > 0 and solution[literal-1]:
                count += 1
                break
            if literal < 0 and not solution[abs((literal+1))]:
                count += 1
                break
    return count


def find_global_max(n: int, clauses: list[list[int]]):
    max_fulfilled = 0
    for solution in product([True, False], repeat=n):
        fulfilled = clauses_fulfilled(clauses, solution)
        if fulfilled > max_fulfilled:
            max_fulfilled = fulfilled
    return max_fulfilled


def generate_clauses(n: int):
    pos = list(range(1, n+1))
    neg = [-v for v in pos]
    lit = pos + neg
    cls = [[v] for v in lit]
    def _gen(cs: list[list[int]]):
        for c1 in cs:
            for c2 in cs:
                pass
    # [[a]]
    # [[b]]
    # [[-a]]
    # [[-b]]
    # [[a b]]
    # [[-a b]]
    # [[a -b]]
    # [[-a -b]]
    # [[-a] [-b]]
    # [[a] [b]]


if __name__ == '__main__':
    cs = [[1, 2], [2, 3], [3, 1]]
    sl = [False, False, False]
    print(find_global_max(3, cs))

