from z3 import Or

from gates import Gate


class OrGate(Gate):
    def to_z3(self, *args):
        return Or(*args)
