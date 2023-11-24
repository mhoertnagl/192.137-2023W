import numpy as np


class DisjointSet:

    def __init__(self, n: int):
        # Constructor to create and initialize sets of n items.
        self.rank = np.ones(n+1, dtype=int)
        self.parent = np.arange(0, n+1, 1, dtype=int)

    def find(self, x: int) -> int:
        """
        Finds the set representative of given item x.
        :param x: Item x for which to find the representative.
        :return: Set representative.
        """
        # Finds the root representative of the set for which
        # x is an element of.
        if self.parent[x] != x:
            # If x is not the parent of itself then x is
            # not the representative of its set, so we
            # recursively call Find on its parent and
            # move i's node directly under the
            # representative of this set.
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int):
        """
        Do union of two sets represented by x and y.
        :param x: Set represented by x.
        :param y: Set represented by y.
        """
        # Find root representatives of the sets for which
        # x and y are elements of.
        sx = self.find(x)
        sy = self.find(y)
        # If they are already in same set.
        if sx == sy:
            return
        # Put smaller ranked item under bigger ranked item
        # if ranks are different.
        if self.rank[sx] < self.rank[sy]:
            self.parent[sx] = sy
        elif self.rank[sx] > self.rank[sy]:
            self.parent[sy] = sx
        # If ranks are same, then move y under x and
        # increment rank of x's tree.
        else:
            self.parent[sy] = sx
            self.rank[sx] = self.rank[sx] + 1

    def connected(self, x: int, y: int):
        """
        Returns True iff the two sets represented by x and y
        are connected.
        :param x: Set represented by x.
        :param y: Set represented by y.
        :return: True iff sets represented by x and y are
                 connected.
        """
        return self.find(x) == self.find(y)

    def size(self, x: int) -> int:
        """
        Returns the size of the set to which item x belongs.
        :param x: Item.
        :return: The size of the set to which item x belongs.
        """
        return self.rank[self.find(x)]
