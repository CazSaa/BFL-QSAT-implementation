from z3 import And

from gates.gate import Gate


class AndGate(Gate):
    def to_z3(self, *args):
        return And(*args)
