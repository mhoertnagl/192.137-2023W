from pathlib import Path
from typing import TextIO

from splex import Problem


def read(filename: str):
    with open(filename) as file:
        return read_file(file)


def read_file(file: TextIO):
    edges = []
    name = _get_file_stem(file)
    line = file.readline()
    (s, n, _, _) = _parse_ints(line)
    while line := file.readline():
        edges.append(_parse_ints(line))
    return Problem(name, s, n, edges)


def _parse_ints(line: str):
    return list(map(int, line.strip().split()))


def _get_file_stem(file: TextIO):
    return Path(file.name).stem
