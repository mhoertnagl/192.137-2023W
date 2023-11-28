#!/usr/bin/env python3
# -*- coding: utf8 -*-
"""
DESCRIPTION GOES HERE
"""

import sys
import traceback
import argparse
import time

from grasper import Grasper
from reader import Reader
from localsearch import LocalSearch
from annealer import Annealer
import detcon as dc
import rancon as rc
import neighborhoods as nhs
from vnd import VND


def main():
    # global args
    reader = Reader()
    # problem = reader.read(args.input)
    problem = reader.read("../inst/testing/test.txt")
    # problem = reader.read("../inst/testing/heur002_n_100_m_3274.txt")
    #problem = reader.read("../inst/testing/heur003_n_120_m_2588.txt")
    # problem = reader.read("../inst/testing/heur004_n_140_m_3014.txt")
    # problem = reader.read("../inst/testing/heur005_n_160_m_4015.txt")
    print(problem)
    # problem.s = 1
    # problem.draw()

    # con = dc.DetCon3(problem)
    con = dc.DetCon2(problem)
    # con = dc.DetCon1(problem)
    # con = rc.RanCon1(problem, 10)
    sol = con.construct()
    print(sol.is_feasible())
    sol.draw()
    print(sol.get_value())

    # nbh = nhs.ComponentMergeNeighborhood(10)
    # ls = LocalSearch(nbh, 1000)
    # sol = ls.run(sol)
    # print(sol.is_feasible())
    # sol.draw()
    # print(sol.get_value())
    
    nbh = nhs.TwoFlipNeighborhood(step_fun="best improvement")
    ls = LocalSearch(nbh, 10)
    sol = ls.run(sol)
    print(sol.is_feasible())
    sol.draw()
    print(sol.get_value())
    

    # nbh1 = nhs.VertexSwapNeighborhood()
    # ls1 = LocalSearch(nbh1, 1000)
    # sol1 = ls1.run(sol)
    # # an = Annealer(sol, nbh1, 50, 0.75)
    # # sol1 = an.run()
    # print(sol1.is_feasible())
    # sol1.draw()
    # print(sol1.get_value())
    #
    # nbh2 = nhs.SingleComponentMultiExchangeNeighborhood()
    # ls2 = LocalSearch(nbh2, 1000)
    # sol2 = ls2.run(sol1)
    # print(sol2.is_feasible())
    # sol2.draw()
    # print(sol2.get_value())

    # nbh = nhs.VertexMoveNeighborhood()
    # ls = LocalSearch(nbh, 1000)
    # con = rc.RanCon1(problem, 10)
    # gsp = Grasper(ls, con, 100)
    # sol = gsp.run()
    # print(sol.is_feasible())
    # sol.draw()
    # print(sol.get_value())

    # nbh1 = nhs.ComponentMergeNeighborhood()
    # nbh2 = nhs.VertexMoveNeighborhood()
    # nbh3 = nhs.TwoExchangeNeighborhood()
    # vnd = VND([nbh1, nbh2, nbh3])
    # con = dc.DetCon2(problem)
    # sol = con.construct()
    # sol = vnd.run(sol)
    # print(sol.is_feasible())
    # sol.draw()
    # print(sol.get_value())


def ran_vs_det():
    reader = Reader()
    problem = reader.read("../inst/testing/heur002_n_100_m_3274.txt")
    # problem = reader.read("../inst/testing/heur003_n_120_m_2588.txt")
    # problem = reader.read("../inst/testing/heur004_n_140_m_3014.txt")
    # problem = reader.read("../inst/testing/heur005_n_160_m_4015.txt")
    # TODO: Exception with this and detcon1
    # problem = reader.read("../inst/testing/heur039_n_361_m_13593.txt")

    rcon = rc.RanCon1(problem, 10)
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
