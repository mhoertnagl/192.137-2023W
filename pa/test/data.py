from splex import Problem, Solution


def problem_4z_s2():
    return Problem("4Z-s2", 2, 4, [
        (1, 2, 1, 2),
        (1, 3, 0, 1),
        (1, 4, 0, 4),
        (2, 3, 1, 3),
        (2, 4, 0, 1),
        (3, 4, 1, 5)
    ])


def solution_4z_s2_01():
    """Value: 2 + 3 + 5 = 10"""
    sol = Solution(problem_4z_s2())
    return sol


def solution_4z_s2_02():
    """Value: 2 + 3 + 5 + 1 + 1 = 12"""
    sol = Solution(problem_4z_s2())
    sol.add_edge(1, 3)
    sol.add_edge(2, 4)
    return sol


def solution_4z_s2_03():
    """Value: 1 + 1 + 3 = 5"""
    sol = Solution(problem_4z_s2())
    sol.add_edge(1, 2)
    sol.add_edge(1, 3)
    sol.add_edge(2, 4)
    sol.add_edge(3, 4)
    return sol


def solution_4z_s2_04():
    """Value: 1 + 1 + 5 + 2 + 4 = 13"""
    sol = Solution(problem_4z_s2())
    sol.add_edge(1, 3)
    sol.add_edge(1, 4)
    sol.add_edge(2, 3)
    sol.add_edge(2, 4)
    return sol


def solution_4z_s2_05():
    """Value: 1 + 1 = 2"""
    sol = Solution(problem_4z_s2())
    sol.add_edge(1, 2)
    sol.add_edge(1, 3)
    sol.add_edge(2, 3)
    sol.add_edge(2, 4)
    sol.add_edge(3, 4)
    return sol


def solution_4z_s2_06():
    """Value: 4 + 1 + 1 = 6"""
    sol = Solution(problem_4z_s2())
    sol.add_edge(1, 2)
    sol.add_edge(1, 3)
    sol.add_edge(1, 4)
    sol.add_edge(2, 3)
    sol.add_edge(2, 4)
    sol.add_edge(3, 4)
    return sol
