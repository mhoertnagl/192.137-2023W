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
from localsearch import LocalSearch
from annealer import Annealer
import detcon as dc
import rancon as rc
import neighborhoods as nhs
import networkx as nx


def main():
    # global args
    reader = Reader()
    # problem = reader.read(args.input)
    # problem = reader.read("../inst/testing/heur002_n_100_m_3274.txt")
    problem = reader.read("../inst/testing/heur003_n_120_m_2588.txt")
    # problem = reader.read("../inst/testing/heur004_n_140_m_3014.txt")
    # problem = reader.read("../inst/testing/heur005_n_160_m_4015.txt")
    print(problem)
    # problem.s = 1
    # print(problem)
    # print(problem.weight(1, 6))
    # print(problem.all_edges_weighted())
    # problem.draw()

    con = dc.DetCon3(problem)
    # con = dc.DetCon2(problem)
    # con = dc.DetCon1(problem)
    # con = rc.RanCon(problem, 10)
    sol = con.construct()
    print(sol.is_feasible())
    sol.draw()
    print(sol.get_value())

    # nbh1 = nhs.VertexSwapNeighborhood()
    # ls1 = LocalSearch(sol, nbh1, 1000)
    # sol1 = ls1.run()
    # # an = Annealer(sol, nbh1, 50, 0.75)
    # # sol1 = an.run()
    # print(sol1.is_feasible())
    # sol1.draw()
    # print(sol1.get_value())
    #
    # nbh2 = nhs.SingleComponentMultiExchangeNeighborhood()
    # ls2 = LocalSearch(sol1, nbh2, 1000)
    # sol2 = ls2.run()
    # print(sol2.is_feasible())
    # sol2.draw()
    # print(sol2.get_value())


def ran_vs_det():
    reader = Reader()
    # problem = reader.read("../inst/testing/heur002_n_100_m_3274.txt")
    # problem = reader.read("../inst/testing/heur003_n_120_m_2588.txt")
    # problem = reader.read("../inst/testing/heur004_n_140_m_3014.txt")
    # problem = reader.read("../inst/testing/heur005_n_160_m_4015.txt")
    problem = reader.read("../inst/testing/heur039_n_361_m_13593.txt")

    rcon = rc.RanCon(problem, 10)
    rsol = rcon.construct()
    print(rsol.is_feasible())
    rsol.draw()
    print(rsol.get_value())

    dcon = dc.DetCon1(problem)
    dsol = dcon.construct()
    print(dsol.is_feasible())
    dsol.draw()
    print(dsol.get_value())

if __name__ == '__main__':
    main()
    # ran_vs_det()
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
