#!/usr/bin/env python3
# -*- coding: utf8 -*-
"""
DESCRIPTION GOES HERE
"""

import sys
import traceback
import argparse
import time

from reader import Reader
from detcon import DetCon1, DetCon2
from localsearch import LocalSearch
import neighborhoods as nhs

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

    nbh1 = nhs.VertexMoveNeighborhood()
    ls1 = LocalSearch(sol, nbh1, 1000)
    sol1 = ls1.run()
    print(sol1.is_feasible())
    sol1.draw()
    print(sol1.get_value())

    nbh2 = nhs.SingleComponentMultiExchangeNeighborhood()
    ls2 = LocalSearch(sol1, nbh2, 1000)
    sol2 = ls2.run()
    print(sol2.is_feasible())
    sol2.draw()
    print(sol2.get_value())


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
