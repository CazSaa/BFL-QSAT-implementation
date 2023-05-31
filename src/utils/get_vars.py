# https://stackoverflow.com/a/14089886/14851412
from z3 import is_const, Ints, Bools, Implies, And, Or, Z3_OP_UNINTERPRETED, \
    AstRef, BoolRef, ForAll


# Wrapper for allowing Z3 ASTs to be stored into Python Hashtables.
class AstRefKey:
    def __init__(self, n):
        self.n = n

    def __hash__(self):
        return self.n.hash()

    def __eq__(self, other):
        return self.n.eq(other.n)

    def __repr__(self):
        return str(self.n)


def askey(n):
    assert isinstance(n, AstRef)
    return AstRefKey(n)


def get_vars(f: BoolRef):
    r = dict()

    def collect(f):
        if is_const(f):
            if f.decl().kind() == Z3_OP_UNINTERPRETED and not askey(f) in r:
                r[askey(f)] = None
        else:
            for c in f.children():
                collect(c)

    collect(f)
    return [e.n for e in r]


if __name__ == '__main__':
    x, y = Ints('x y')
    a, b = Bools('a b')
    r = ForAll(a, Or(a, b))
    print(get_vars(
        Implies(And(x + y == 0, x * 2 == 10), Or(a, Implies(a, b == False)))))
