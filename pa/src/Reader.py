from pathlib import Path
from typing import TextIO

from Problem import Problem


class Reader:

    def read(self, filename: str):
        with open(filename) as file:
            name = get_file_stem(file)
            (s, n) = parse_ints(file.readline())
            edges = self.__read_edges(file)
            return Problem(name, s, n, edges)

    def __read_edges(self, file: TextIO):
        edges = []
        while line := file.readline():
            edges.append(parse_ints(line))
        return edges


def parse_ints(line: str):
    return list(map(int, line.strip().split()))


def get_file_stem(file: TextIO):
    return Path(file.name).stem
