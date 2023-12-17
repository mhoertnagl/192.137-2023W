from abc import ABC, abstractmethod


class Problem(ABC):

    @abstractmethod
    def name(self):
        pass
