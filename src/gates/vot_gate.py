from typing import Literal

allowed_comparisons = {'<', '<=', '==', '>=', '>'}
VotComp = Literal['<', '<=', '==', '>=', '>']


class VotGate:
    def __init__(self, comp: VotComp, k: int):
        if comp not in allowed_comparisons:
            raise ValueError('Unknown comp')

        self.comp = comp
        self.k = k
