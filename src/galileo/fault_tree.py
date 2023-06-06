import networkx as nx
from z3 import BoolRef, Bool


class FaultTree(nx.DiGraph):
    def get_basic_events(self) -> list[str]:
        # noinspection PyTypeChecker
        return [node for (node, in_deg) in self.in_degree if in_deg == 0]

    def get_basic_events_set(self) -> set[str]:
        # noinspection PyTypeChecker
        return {node for (node, in_deg) in self.in_degree if in_deg == 0}

    def get_basic_events_bools(self) -> list[BoolRef]:
        # noinspection PyTypeChecker
        return [Bool(node) for (node, in_deg) in self.in_degree if in_deg == 0]
