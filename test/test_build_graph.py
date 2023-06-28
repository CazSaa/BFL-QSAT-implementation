import unittest

import networkx as nx
from networkx.utils import nodes_equal

from galileo.build_graph import build_fault_tree
from galileo.exceptions import EventAlreadyDefinedError, NotAcyclicError, \
    NotExactlyOneRootError
from gates import AndGate, OrGate, VotGate
from parser.parser import parse


def my_graph_equals(graph1: nx.Graph, graph2: nx.Graph):
    return graph1.adj == graph2.adj \
           and nodes_equal(graph1.nodes, graph2.nodes) \
           and graph1.graph == graph2.graph


class BuildGraphTest(unittest.TestCase):
    def test_build_graph(self):
        tree = parse('''
        toplevel top;
        top and a b c;
        a or d e;
        d 2of3 f g h;
        h vot<=2 i j k l;
        ---
        [[a]];
        ''')
        graph = build_fault_tree(tree)
        graph2 = nx.DiGraph()
        graph2.add_node('top', gate=AndGate())
        graph2.add_node('a', gate=OrGate())
        graph2.add_node('d', gate=VotGate('>=', 2))
        graph2.add_node('h', gate=VotGate('<=', 2))
        graph2.add_edges_from([
            ('a', 'top'), ('b', 'top'), ('c', 'top'), ('d', 'a'), ('e', 'a'),
            ('f', 'd'), ('g', 'd'), ('h', 'd'), ('i', 'h'), ('j', 'h'),
            ('k', 'h'), ('l', 'h')])
        self.assertTrue(my_graph_equals(graph, graph2))

    def test_order_does_not_matter(self):
        graph1 = build_fault_tree(parse('''
        toplevel top;
        top and a b c;
        a or d e;
        d 2of3 f g h;
        h vot>=2 i j k l;
        ---
        [[a]];
        '''))
        graph2 = build_fault_tree(parse('''
        toplevel top;
        h vot>=2 i j k l;
        d 2of3 f g h;
        a or d e;
        top and a b c;
        ---
        [[a]];
        '''))
        self.assertTrue(my_graph_equals(graph1, graph2))

    def test_can_define_basic_events_explicitly(self):
        graph1 = build_fault_tree(parse('''
        toplevel top;
        top and a b c;
        a or d e;
        d 2of3 f g h;
        h vot>=2 i j k l;
        ---
        [[a]];
        '''))
        graph2 = build_fault_tree(parse('''
        toplevel top;
        d 2of3 f g h;
        a or d e;
        h vot>=2 i j k l;
        f;
        g;
        k;
        l;
        top and a b c;
        ---
        [[a]];
        '''))
        self.assertTrue(my_graph_equals(graph1, graph2))

    def test_cannot_redefine_events(self):
        self.assertRaises(
            EventAlreadyDefinedError,
            lambda: build_fault_tree(parse('''
                toplevel top;
                top and a b c;
                a or d e;
                a and m n;
                d 2of3 f g h;
                d;
                h vot>=2 i j k l;
                ---
                [[a]];
            '''))
        )

    def test_cannot_contain_cycles(self):
        self.assertRaises(
            NotAcyclicError,
            lambda: build_fault_tree(parse('''
                toplevel top;
                top or a;
                a or b;
                b or top;
                ---
                [[a]];
            '''))
        )

    def test_only_top_event(self):
        graph1 = build_fault_tree(parse('''
            toplevel top;
            ---
            [[a]];
        '''))
        graph2 = nx.DiGraph()
        graph2.add_node('top')
        self.assertTrue(my_graph_equals(graph1, graph2))

    def test_can_only_have_one_root(self):
        self.assertRaises(
            NotExactlyOneRootError,
            lambda: build_fault_tree(parse('''
                toplevel top;
                a or b;
                ---
                [[a]];
            '''))
        )


if __name__ == '__main__':
    unittest.main()
