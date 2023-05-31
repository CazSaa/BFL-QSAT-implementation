import unittest

from galileo.fault_tree import FaultTree
from gates import AndGate, OrGate


class FaultTreeTest(unittest.TestCase):
    def test_basic_events(self):
        ft = FaultTree()
        ft.add_node('top', gate=AndGate())
        ft.add_node('a')
        ft.add_edge('a', 'top')

        ft.add_node('b', gate=OrGate())
        ft.add_edge('b', 'top')

        ft.add_node('c')
        ft.add_edge('c', 'b')

        ft.add_node('d')
        ft.add_edge('d', 'b')

        self.assertListEqual(['a', 'c', 'd'], ft.get_basic_events())


if __name__ == '__main__':
    unittest.main()
