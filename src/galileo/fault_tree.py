import networkx as nx
from z3 import BoolRef, Bool


class FaultTree(nx.DiGraph):
    def get_basic_events(self) -> list[str]:
        return [node for (node, in_deg) in self.in_degree if in_deg == 0]

    def get_basic_events_set(self) -> set[str]:
        return {node for (node, in_deg) in self.in_degree if in_deg == 0}

    def get_basic_events_bools(self) -> list[BoolRef]:
        return [Bool(node) for (node, in_deg) in self.in_degree if in_deg == 0]

    def get_root(self) -> str:
        return next((node for (node, out_deg) in self.out_degree
                     if out_deg == 0))
