import networkx as nx


class FaultTree(nx.DiGraph):
    def get_basic_events(self) -> list[str]:
        # noinspection PyTypeChecker
        return [node for (node, in_deg) in self.in_degree if in_deg == 0]
