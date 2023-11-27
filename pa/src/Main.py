#!/usr/bin/env python3
# -*- coding: utf8 -*-
"""
DESCRIPTION GOES HERE
"""

import sys
import traceback
import argparse
import time

from localsearch import LocalSearch
from neighborhoods import OneFlipNeighborhood, VertexMoveNeighborhood
from reader import Reader
from detcon import DetCon1, DetCon2


def main():
    # global args
    reader = Reader()
    # problem = reader.read(args.input)
    problem = reader.read("../inst/testing/heur002_n_100_m_3274.txt")
    # problem.s = 1
    # print(problem)
    # print(problem.weight(1, 6))
    # print(problem.all_edges_weighted())
    # problem.draw()

    con = DetCon1(problem)
    # con = DetCon2(problem)
    sol = con.construct()
    sol.draw()
    print(sol.get_value())

    nbh = VertexMoveNeighborhood()
    ls = LocalSearch(sol, nbh, 1000)
    new_sol = ls.run()
    new_sol.draw()
    print(new_sol.get_value())


if __name__ == '__main__':
    main()
    # try:
    #     start_time = time.time()
    #     parser = argparse.ArgumentParser(description=__doc__)
    #     parser.add_argument('input')
    #     parser.add_argument('-v', '--version', action='version', version='0.0.1')
    #     args = parser.parse_args()
    #     main()
    #     print("Total running time in seconds: %0.2f" % (time.time() - start_time))
    #     sys.exit(0)
    # except KeyboardInterrupt as e:
    #     raise e
    # except SystemExit as e:
    #     raise e
    # except Exception as e:
    #     print('ERROR, UNEXPECTED EXCEPTION')
    #     print(str(e))
    #     traceback.print_exc()
    #     sys.exit(1)
