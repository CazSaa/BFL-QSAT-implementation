# https://theory.stanford.edu/~nikolaj/programmingz3.html#sec-blocking-evaluations
from z3 import sat


def all_models(s, initial_terms):
    def block_term(s_, m, t):
        s_.add(t != m.eval(t, model_completion=True))

    def fix_term(s_, m, t):
        s_.add(t == m.eval(t, model_completion=True))

    def all_smt_rec(terms):
        if sat == s.check():
            m = s.model()
            yield m
            for i in range(len(terms)):
                s.push()
                block_term(s, m, terms[i])
                for j in range(i):
                    fix_term(s, m, terms[j])
                yield from all_smt_rec(terms[i:])
                s.pop()

    yield from all_smt_rec(list(initial_terms))
