from abc import ABC

from benchy import ISolution


class Solution(ISolution, ABC):

    def value(self) -> int | float:
        pass