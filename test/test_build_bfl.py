import unittest

from z3 import BoolRef, Solver, Not, unsat, Bools, And, Or, Implies, eq, \
    ForAll, Exists, Function, BoolSort, AtLeast, AtMost

from bfl.build_bfl import BflTransformer, event_to_formula
from galileo.build_graph import build_fault_tree
from galileo.fault_tree import FaultTree
from parser.parser import parser

default_tree = build_fault_tree(
    parser.parse('toplevel top; top or a b c;', 'galileo'))


def z3_equality(formula1: BoolRef, formula2: BoolRef):
    s = Solver()
    s.add(Not(formula1 == formula2))
    return s.check() == unsat


def parse_helper(formula: str, start='bfl_statement', tree=default_tree):
    return BflTransformer(tree).transform(parser.parse(formula, start))


class BuildBflTest(unittest.TestCase):
    def test_simple_connectives(self):
        a, b = Bools('a b')

        self.assertTrue(eq(parse_helper('a && b', 'phi'), And(a, b)))
        self.assertTrue(eq(parse_helper('a || b', 'phi'), Or(a, b)))
        self.assertTrue(eq(parse_helper('a => b', 'phi'), Implies(a, b)))
        # noinspection PyTypeChecker
        self.assertTrue(eq(parse_helper('a == b', 'phi'), a == b))
        # noinspection PyTypeChecker
        self.assertTrue(eq(parse_helper('a != b', 'phi'), a != b))
        self.assertTrue(eq(parse_helper('!a', 'phi'), Not(a)))

    def test_quantifiers(self):
        a, b, c = Bools('a b c')
        self.assertTrue(eq(
            parse_helper('\\forall a || b'),
            ForAll([a, b], Or(a, b))
        ))
        self.assertTrue(eq(
            parse_helper('\\exists a || b'),
            Exists([a, b], Or(a, b))
        ))

    def test_setting_evidence(self):
        a, b, c = Bools('a b c')
        self.assertTrue(eq(
            parse_helper('\\exists a && b [a:1,b:0,c:0]'),
            ForAll([a, b, c], Implies(And(a, Not(b), Not(c)), And(a, b)))
        ))
        self.assertTrue(eq(
            parse_helper('\\exists a || b && c [b:0]'),
            Exists([a, c], ForAll(b, Implies(Not(b), Or(a, And(b, c)))))
        ))

    def test_evidence_quantifier_arrangement_equality(self):
        a, b = Bools('a b')
        f = Function('f', BoolSort(), BoolSort(), BoolSort())
        self.assertTrue(z3_equality(
            ForAll([a], Implies(a, ForAll([b], Implies(Not(b), f(a, b))))),
            ForAll([a, b], Implies(And(a, Not(b)), f(a, b)))
        ))

    def test_mcs(self):
        a, b, c, a_, b_, c_ = Bools("a b c a' b' c'")
        self.assertTrue(eq(
            parse_helper('\\exists \\mcs(a)'),
            Exists(
                [a, b, c],
                And(
                    a,
                    Not(Exists(
                        [a_, b_, c_],
                        And(
                            And(Implies(a_, a), Implies(b_, b), Implies(c_, c)),
                            Or(a_ != a, b_ != b, c_ != c),
                            a_
                        )
                    ))
                )
            )
        ))

    def test_two_mcs(self):
        a, b, c, a_, b_, c_, a__, b__, c__ = Bools("a b c a' b' c' a'' b'' c''")
        self.assertTrue(eq(
            parse_helper('\\exists \\mcs(a) && \\mcs(b)'),
            Exists(
                [a, b, c],
                And(
                    And(
                        a,
                        Not(Exists(
                            [a_, b_, c_],
                            And(
                                And(Implies(a_, a), Implies(b_, b),
                                    Implies(c_, c)),
                                Or(a_ != a, b_ != b, c_ != c),
                                a_
                            )
                        ))
                    ),
                    And(
                        b,
                        Not(Exists(
                            [a__, b__, c__],
                            And(
                                And(Implies(a__, a), Implies(b__, b),
                                    Implies(c__, c)),
                                Or(a__ != a, b__ != b, c__ != c),
                                b__
                            )
                        ))
                    )
                )
            )

        ))

    def test_mps(self):
        a, b, c, a_, b_, c_ = Bools("a b c a' b' c'")
        self.assertTrue(eq(
            parse_helper('\\exists \\mps(a)'),
            Exists(
                [a, b, c],
                And(
                    Not(a),
                    Not(Exists(
                        [a_, b_, c_],
                        And(
                            And(Implies(a_, a), Implies(b_, b), Implies(c_, c)),
                            Or(a_ != a, b_ != b, c_ != c),
                            Not(a_)
                        )
                    ))
                )
            )
        ))

    def test_event_to_formula(self):
        bigger_tree = build_fault_tree(
            parser.parse('toplevel top;'
                         'top or a b c l p;'
                         'a and d e;'
                         'b 2of3 f g h;'
                         'c vot<3 i j k;'
                         'l vot==2 m n o;'
                         'p vot <=1 q r;'
                         'q vot>=1 s t;'
                         's vot >1 u v;', 'galileo'))
        a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, s, t, u, v = \
            Bools('a b c d e f g h i j k l m n o p q r s t u v')
        self.assertTrue(eq(
            parse_helper('top', 'phi', tree=bigger_tree),
            Or(
                And(d, e),
                AtLeast(f, g, h, 2),
                AtMost(i, j, k, 2),
                And(AtLeast(m, n, o, 2), AtMost(m, n, o, 2)),
                AtMost(AtLeast(AtLeast(u, v, 2), t, 1), r, 1),
            )
        ))

    def test_unknown_event_error(self):
        self.assertRaises(
            ValueError,
            lambda: event_to_formula('e', default_tree)
        )

    def test_no_gate_error(self):
        tree = FaultTree()
        tree.add_node('top')
        tree.add_node('a')
        tree.add_edge('a', 'top')
        self.assertRaises(
            ValueError,
            lambda: event_to_formula('top', tree)
        )


if __name__ == '__main__':
    unittest.main()
