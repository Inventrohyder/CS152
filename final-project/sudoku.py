from pyswip import Prolog
from pyswip.easy import Functor, Term, Variable, call, registerForeign


prolog = Prolog()

prolog.consult('sudoku_for_py.pl')

problem = Functor("problem", 2)

def solve_problem(prob: str) -> str:

    retractall = Functor("retractall")
    # Each we query clear all the problems values
    call(retractall(problem))

    prolog.assertz(f"""problem(1, {prob})""")

    return list(prolog.query('answer(X).', maxresult=1))[0]['X']

