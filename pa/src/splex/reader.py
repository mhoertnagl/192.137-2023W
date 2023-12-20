import os
from pathlib import Path
from typing import TextIO

from splex import Problem


def read_dir(path: str):
    for item in os.listdir(path):
        filename = os.path.join(path, item)
        if os.path.isfile(filename):
            yield read_file(filename)


def read_file(filename: str):
    with open(filename) as file:
        return _read_file(file)


def _read_file(file: TextIO):
    edges = []
    name = Path(file.name).stem
    line = file.readline()
    (s, n, _, _) = _parse_ints(line)
    while line := file.readline():
        edges.append(_parse_ints(line))
    return Problem(name, s, n, edges)


def _parse_ints(line: str):
    return list(map(int, line.strip().split()))
