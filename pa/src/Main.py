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


def main():
    global args
    reader = Reader()
    problem = reader.read(args.input)
    problem.s = 3
    # print(problem)
    # print(problem.weight(1, 6))
    # print(problem.all_edges_weighted())
    # problem.draw()

    con = DetCon1(problem)
    # con = DetCon2(problem)
    solution = con.construct()
    solution.draw()
    print(solution.evaluate())


if __name__ == '__main__':
    try:
        start_time = time.time()
        parser = argparse.ArgumentParser(description=__doc__)
        parser.add_argument('input')
        parser.add_argument('-v', '--version', action='version', version='0.0.1')
        args = parser.parse_args()
        main()
        print("Total running time in seconds: %0.2f" % (time.time() - start_time))
        sys.exit(0)
    except KeyboardInterrupt as e:
        raise e
    except SystemExit as e:
        raise e
    except Exception as e:
        print('ERROR, UNEXPECTED EXCEPTION')
        print(str(e))
        traceback.print_exc()
        sys.exit(1)
