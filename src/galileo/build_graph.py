import networkx as nx
from lark import Tree
from networkx import is_directed_acyclic_graph

from gates import AndGate, OrGate, VotGate
from galileo.exceptions import EventAlreadyDefinedError, NotAcyclicError, \
    NotExactlyOneRootError


def get_galileo_tree(parse_tree: Tree):
    if parse_tree.data == 'galileo':
        return parse_tree
    if parse_tree.data == 'start':
        assert parse_tree.children[0].data == 'galileo'
        return parse_tree.children[0]
    raise ValueError(f'parse_tree does not contain galileo tree: {parse_tree}')


def get_gate(gate: Tree):
    match gate.data:
        case 'and_gate':
            return AndGate()
        case 'or_gate':
            return OrGate()
        case 'vot_gate':
            return VotGate(gate.children[0], int(gate.children[1]))
        case 'of_gate':
            return VotGate('>=', gate.children[0])


def build_graph(parse_tree: Tree):
    galileo_tree = get_galileo_tree(parse_tree)
    graph = nx.DiGraph()
    defined_events = set()

    for line in galileo_tree.children:
        match line.data:
            case 'tle':
                graph.add_node(line.children[0].value)

            case 'intermediate_event':
                [event, gate, *children] = line.children
                if event in defined_events:
                    raise EventAlreadyDefinedError()

                graph.add_node(event.value, gate=get_gate(gate))
                for child in children:
                    graph.add_edge(child.value, event.value)
                defined_events.add(event)

            case 'basic_event':
                event = line.children[0]
                if event in defined_events:
                    raise EventAlreadyDefinedError()
                graph.add_node(event.value)
                defined_events.add(event)

    if not is_directed_acyclic_graph(graph):
        raise NotAcyclicError()

    # noinspection PyTypeChecker
    if sum(1 for (node, out) in graph.out_degree if out == 0) != 1:
        raise NotExactlyOneRootError()

    return graph
