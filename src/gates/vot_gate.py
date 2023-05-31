from typing import Literal

from z3 import AtMost, AtLeast, And

from gates import Gate

allowed_comparisons = {'<', '<=', '==', '>=', '>'}
VotComp = Literal['<', '<=', '==', '>=', '>']


class VotGate(Gate):
    def __init__(self, comp: VotComp, k: int):
        if comp not in allowed_comparisons:
            raise ValueError('Unknown comp')

        self.comp = comp
        self.k = k

    def to_z3(self, *args):
        match self.comp:
            case '<':
                return AtMost(*args, self.k - 1)
            case '<=':
                return AtMost(*args, self.k)
            case '>':
                return AtLeast(*args, self.k + 1)
            case '>=':
                return AtLeast(*args, self.k)
            case '==':
                return And(AtLeast(*args, self.k), AtMost(*args, self.k))
            case _:
                raise ValueError('Unknown comp')

