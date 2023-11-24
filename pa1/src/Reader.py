from pathlib import Path
from typing import TextIO

from parse import compile, parse

from Instance import Instance


class Reader:
    """
    Reads an instance of the s-plex problem.
    """
    PARAMS_FORMAT = '{s:d} {n:d} {m:d} {l:d}'
    ROW_FORMAT = '{s:d} {t:d} {p:d} {w:d}'

    def __init__(self):
        self.row_pattern = compile(self.ROW_FORMAT)

    def read(self, filename: str) -> Instance:
        """
        Reads an s-plex specification file.
        :param filename: The file name.
        """
        with open(filename) as file:
            return self.read_file(file)

    def read_file(self, file: TextIO) -> Instance:
        """
        Reads an s-plex specification file.
        :param file: The file object.
        """
        name = Path(file.name).stem
        res = parse(self.PARAMS_FORMAT, file.readline().strip())
        instance = Instance(name, res['s'], res['n'], res['m'])
        while line := file.readline():
            res = self.row_pattern.parse(line.strip())
            s, t, p, w = res['s'], res['t'], res['p'], res['w']
            instance.set_edge(s, t, p, w)
        instance.finish()
        return instance
