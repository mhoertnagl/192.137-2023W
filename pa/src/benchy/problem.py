from abc import ABC, abstractmethod


class IProblem(ABC):

    @abstractmethod
    def name(self):
        pass
