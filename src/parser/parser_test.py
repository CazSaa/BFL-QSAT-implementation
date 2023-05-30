import unittest

from lark import Tree, Token

from .parser import parse


class ParserTest(unittest.TestCase):
    def test_parser(self):
        self.assertEqual(
            parse('''
        toplevel top;
        top and a b c;
        b Or or d;
        c orOr ca;
        d 2oF4 e f g h;
        e vOt<2 i j k;
        l;
        
        ---
        \\forall i => (!a || b) && (c == d) != e == f != g;
        
        \\forall(IS => MoT);
        
        \\foRall(MoT => (H1 || H2 && H3 || H4 || H5));
        
        \\foraLl H4 => IWoS; // parentheses not mandatory
        
        \\forall(\\vot[>= 2](H1,H2,H3,H4,H5) => IWoS);
        
        [[\\mcs(IWoS) && H4]];
        
        \\eXists \\mps(IWoS)[H1: 0, H2: 0,H3: 0,H4: 0,H5: 0];
        
        \\idP(CIO,CIS);
        
        \\SUP(PP);
        
        UT, IW, H3 |= CPR && MoT;
        
        \\forall (CPR == CIW);
        
        \\forall (CPR != CIW);
        
        \\forall (!IS => !CIS);
        '''),
            Tree(Token('RULE', 'start'), [
                Tree(Token('RULE', 'galileo'), [
                    Tree(Token('RULE', 'tle'),
                         [Token('EVENT_NAME', 'top')]),
                    Tree(Token('RULE', 'intermediate_event'),
                         [Token('EVENT_NAME', 'top'),
                          Tree('and_gate', []),
                          Token('EVENT_NAME', 'a'),
                          Token('EVENT_NAME', 'b'),
                          Token('EVENT_NAME', 'c')]),
                    Tree(Token('RULE', 'intermediate_event'),
                         [Token('EVENT_NAME', 'b'),
                          Tree('or_gate', []),
                          Token('EVENT_NAME', 'or'),
                          Token('EVENT_NAME', 'd')]),
                    Tree(Token('RULE', 'intermediate_event'),
                         [Token('EVENT_NAME', 'c'),
                          Tree('or_gate', []),
                          Token('EVENT_NAME', 'Or'),
                          Token('EVENT_NAME', 'ca')]),
                    Tree(Token('RULE', 'intermediate_event'),
                         [Token('EVENT_NAME', 'd'),
                          Tree('of_gate',
                               [Token('INT', '2'), Token('INT', '4')]),
                          Token('EVENT_NAME', 'e'),
                          Token('EVENT_NAME', 'f'),
                          Token('EVENT_NAME', 'g'),
                          Token('EVENT_NAME', 'h')]),
                    Tree(Token('RULE', 'intermediate_event'),
                         [Token('EVENT_NAME', 'e'),
                          Tree('vot_gate', [Token('RELATION', '<'),
                                            Token('INT', '2')]),
                          Token('EVENT_NAME', 'i'),
                          Token('EVENT_NAME', 'j'),
                          Token('EVENT_NAME', 'k')]),
                    Tree(Token('RULE', 'basic_event'), [
                        Token('EVENT_NAME', 'l')])]),
                Tree(Token('RULE', 'bfl'), [
                    Tree(Token('RULE', 'bfl_statement'), [
                        Tree('forall', [
                            Tree(Token('RULE', 'implies'), [
                                Tree('basic_event',
                                     [Token('BASIC_EVENT', 'i')]),
                                Tree(Token('RULE', 'and'), [
                                    Tree(Token('RULE', 'or'), [
                                        Tree('neg', [
                                            Tree('basic_event', [
                                                Token(
                                                    'BASIC_EVENT',
                                                    'a')])]),
                                        Tree('basic_event', [
                                            Token('BASIC_EVENT',
                                                  'b')])]),
                                    Tree('nequiv', [
                                        Tree('equiv', [
                                            Tree('basic_event',
                                                 [Token('BASIC_EVENT', 'c')]),
                                            Tree('basic_event',
                                                 [Token('BASIC_EVENT', 'd')])
                                        ]),
                                        Tree('equiv', [
                                            Tree('basic_event',
                                                 [Token('BASIC_EVENT', 'e')]),
                                            Tree('nequiv', [
                                                Tree('basic_event', [
                                                    Token('BASIC_EVENT', 'f')]),
                                                Tree('basic_event',
                                                     [Token('BASIC_EVENT',
                                                            'g')])])]
                                             )])])])])]),
                    Tree(Token('RULE', 'bfl_statement'), [
                        Tree('forall', [
                            Tree(Token('RULE', 'implies'), [
                                Tree('basic_event',
                                     [Token('BASIC_EVENT', 'IS')]),
                                Tree('basic_event', [
                                    Token('BASIC_EVENT',
                                          'MoT')])])])]),
                    Tree(Token('RULE', 'bfl_statement'), [
                        Tree('forall', [
                            Tree(Token('RULE', 'implies'), [
                                Tree('basic_event', [
                                    Token('BASIC_EVENT', 'MoT')]),
                                Tree(Token('RULE', 'or'), [
                                    Tree('basic_event', [
                                        Token('BASIC_EVENT',
                                              'H1')]),
                                    Tree(Token('RULE', 'or'), [
                                        Tree(Token('RULE', 'and'),
                                             [Tree('basic_event', [
                                                 Token(
                                                     'BASIC_EVENT',
                                                     'H2')]),
                                              Tree('basic_event', [
                                                  Token(
                                                      'BASIC_EVENT',
                                                      'H3')])]),
                                        Tree(Token('RULE', 'or'), [
                                            Tree('basic_event', [
                                                Token(
                                                    'BASIC_EVENT',
                                                    'H4')]),
                                            Tree('basic_event', [
                                                Token(
                                                    'BASIC_EVENT',
                                                    'H5')])])])])])])]),
                    Tree(Token('RULE', 'bfl_statement'), [
                        Tree('forall', [
                            Tree(Token('RULE', 'implies'), [
                                Tree('basic_event',
                                     [Token('BASIC_EVENT', 'H4')]),
                                Tree('basic_event', [
                                    Token('BASIC_EVENT',
                                          'IWoS')])])])]),
                    Tree(Token('RULE', 'bfl_statement'), [
                        Tree('forall', [
                            Tree(Token('RULE', 'implies'), [
                                Tree('vot',
                                     [Token('RELATION', '>='),
                                      Token('INT', '2'), Tree(
                                         Token('RULE',
                                               'basic_events'), [
                                             Token('BASIC_EVENT',
                                                   'H1'),
                                             Token('BASIC_EVENT',
                                                   'H2'),
                                             Token('BASIC_EVENT',
                                                   'H3'),
                                             Token('BASIC_EVENT',
                                                   'H4'),
                                             Token('BASIC_EVENT',
                                                   'H5')])]),
                                Tree('basic_event', [
                                    Token('BASIC_EVENT',
                                          'IWoS')])])])]),
                    Tree('satisfaction_set', [
                        Tree(Token('RULE', 'and'), [Tree('mcs', [
                            Tree('basic_event',
                                 [Token('BASIC_EVENT', 'IWoS')])]),
                                                    Tree(
                                                        'basic_event',
                                                        [Token(
                                                            'BASIC_EVENT',
                                                            'H4')])])]),
                    Tree(Token('RULE', 'bfl_statement'), [
                        Tree('exists', [Tree('with_evidence', [
                            Tree('mps', [Tree('basic_event', [
                                Token('BASIC_EVENT', 'IWoS')])]),
                            Tree(Token('RULE', 'evidence'), [
                                Tree(Token('RULE', 'mapping'),
                                     [Token('BASIC_EVENT', 'H1'),
                                      Token('TRUTH_VALUE', '0')]),
                                Tree(Token('RULE', 'mapping'),
                                     [Token('BASIC_EVENT', 'H2'),
                                      Token('TRUTH_VALUE', '0')]),
                                Tree(Token('RULE', 'mapping'),
                                     [Token('BASIC_EVENT', 'H3'),
                                      Token('TRUTH_VALUE', '0')]),
                                Tree(Token('RULE', 'mapping'),
                                     [Token('BASIC_EVENT', 'H4'),
                                      Token('TRUTH_VALUE', '0')]),
                                Tree(Token('RULE', 'mapping'),
                                     [Token('BASIC_EVENT', 'H5'),
                                      Token('TRUTH_VALUE',
                                            '0')])])])])]),
                    Tree(Token('RULE', 'bfl_statement'), [
                        Tree('idp', [Tree('basic_event', [
                            Token('BASIC_EVENT', 'CIO')]),
                                     Tree('basic_event', [
                                         Token('BASIC_EVENT',
                                               'CIS')])])]),
                    Tree(Token('RULE', 'bfl_statement'), [
                        Tree('sup', [Tree('basic_event', [
                            Token('BASIC_EVENT', 'PP')])])]),
                    Tree('check_model', [
                        Tree(Token('RULE', 'basic_events'),
                             [Token('BASIC_EVENT', 'UT'),
                              Token('BASIC_EVENT', 'IW'),
                              Token('BASIC_EVENT', 'H3')]),
                        Tree(Token('RULE', 'and'), [
                            Tree('basic_event',
                                 [Token('BASIC_EVENT', 'CPR')]),
                            Tree('basic_event', [
                                Token('BASIC_EVENT', 'MoT')])])]),
                    Tree(Token('RULE', 'bfl_statement'), [
                        Tree('forall', [Tree('equiv', [
                            Tree('basic_event',
                                 [Token('BASIC_EVENT', 'CPR')]),
                            Tree('basic_event', [
                                Token('BASIC_EVENT',
                                      'CIW')])])])]),
                    Tree(Token('RULE', 'bfl_statement'), [
                        Tree('forall', [Tree('nequiv', [
                            Tree('basic_event',
                                 [Token('BASIC_EVENT', 'CPR')]),
                            Tree('basic_event', [
                                Token('BASIC_EVENT',
                                      'CIW')])])])]),
                    Tree(Token('RULE', 'bfl_statement'), [
                        Tree('forall', [
                            Tree(Token('RULE', 'implies'), [
                                Tree('neg', [Tree('basic_event', [
                                    Token('BASIC_EVENT', 'IS')])]),
                                Tree('neg', [Tree('basic_event', [
                                    Token('BASIC_EVENT',
                                          'CIS')])])])])])])])
        )

    def test_print_result(self):
        print(parse('''
        toplevel top;
        top and a b c;
        b Or or d;
        c orOr ca;
        d 2oF4 e f g h;
        e vOt<2 i j k;
        l;
        
        ---
        \\forall i => (!a || b) && (c == d) != e == f != g;
        
        \\forall(IS => MoT);
        
        \\foRall(MoT => (H1 || H2 && H3 || H4 || H5));
        
        \\foraLl H4 => IWoS; // parentheses not mandatory
        
        \\forall(\\vot[>= 2](H1,H2,H3,H4,H5) => IWoS);
        
        [[\\mcs(IWoS) && H4]];
        
        \\eXists \\mps(IWoS)[H1: 0, H2: 0,H3: 0,H4: 0,H5: 0];
        
        \\idP(CIO,CIS);
        
        \\SUP(PP);
        
        UT, IW, H3 |= CPR && MoT;
        
        \\forall (CPR == CIW);
        
        \\forall (CPR != CIW);
        
        \\forall (!IS => !CIS);
        ''').pretty())
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
