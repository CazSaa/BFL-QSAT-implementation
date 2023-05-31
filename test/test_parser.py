import unittest

from lark import Tree, Token

from parser.parser import parse


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
                                Tree('event',
                                     [Token('EVENT_NAME', 'i')]),
                                Tree(Token('RULE', 'and_'), [
                                    Tree(Token('RULE', 'or_'), [
                                        Tree('neg', [
                                            Tree('event', [
                                                Token(
                                                    'EVENT_NAME',
                                                    'a')])]),
                                        Tree('event', [
                                            Token('EVENT_NAME',
                                                  'b')])]),
                                    Tree('nequiv', [
                                        Tree('equiv', [
                                            Tree('event',
                                                 [Token('EVENT_NAME', 'c')]),
                                            Tree('event',
                                                 [Token('EVENT_NAME', 'd')])
                                        ]),
                                        Tree('equiv', [
                                            Tree('event',
                                                 [Token('EVENT_NAME', 'e')]),
                                            Tree('nequiv', [
                                                Tree('event', [
                                                    Token('EVENT_NAME', 'f')]),
                                                Tree('event',
                                                     [Token('EVENT_NAME',
                                                            'g')])])]
                                             )])])])])]),
                    Tree(Token('RULE', 'bfl_statement'), [
                        Tree('forall', [
                            Tree(Token('RULE', 'implies'), [
                                Tree('event',
                                     [Token('EVENT_NAME', 'IS')]),
                                Tree('event', [
                                    Token('EVENT_NAME',
                                          'MoT')])])])]),
                    Tree(Token('RULE', 'bfl_statement'), [
                        Tree('forall', [
                            Tree(Token('RULE', 'implies'), [
                                Tree('event', [
                                    Token('EVENT_NAME', 'MoT')]),
                                Tree(Token('RULE', 'or_'), [
                                    Tree('event', [
                                        Token('EVENT_NAME',
                                              'H1')]),
                                    Tree(Token('RULE', 'or_'), [
                                        Tree(Token('RULE', 'and_'),
                                             [Tree('event', [
                                                 Token(
                                                     'EVENT_NAME',
                                                     'H2')]),
                                              Tree('event', [
                                                  Token(
                                                      'EVENT_NAME',
                                                      'H3')])]),
                                        Tree(Token('RULE', 'or_'), [
                                            Tree('event', [
                                                Token(
                                                    'EVENT_NAME',
                                                    'H4')]),
                                            Tree('event', [
                                                Token(
                                                    'EVENT_NAME',
                                                    'H5')])])])])])])]),
                    Tree(Token('RULE', 'bfl_statement'), [
                        Tree('forall', [
                            Tree(Token('RULE', 'implies'), [
                                Tree('event',
                                     [Token('EVENT_NAME', 'H4')]),
                                Tree('event', [
                                    Token('EVENT_NAME',
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
                                Tree('event', [
                                    Token('EVENT_NAME',
                                          'IWoS')])])])]),
                    Tree('satisfaction_set', [
                        Tree(Token('RULE', 'and_'), [Tree('mcs', [
                            Tree('event',
                                 [Token('EVENT_NAME', 'IWoS')])]),
                                                    Tree(
                                                        'event',
                                                        [Token(
                                                            'EVENT_NAME',
                                                            'H4')])])]),
                    Tree(Token('RULE', 'bfl_statement'), [
                        Tree('exists', [Tree('with_evidence', [
                            Tree('mps', [Tree('event', [
                                Token('EVENT_NAME', 'IWoS')])]),
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
                        Tree('idp', [Tree('event', [
                            Token('EVENT_NAME', 'CIO')]),
                                     Tree('event', [
                                         Token('EVENT_NAME',
                                               'CIS')])])]),
                    Tree(Token('RULE', 'bfl_statement'), [
                        Tree('sup', [Tree('event', [
                            Token('EVENT_NAME', 'PP')])])]),
                    Tree('check_model', [
                        Tree(Token('RULE', 'basic_events'),
                             [Token('BASIC_EVENT', 'UT'),
                              Token('BASIC_EVENT', 'IW'),
                              Token('BASIC_EVENT', 'H3')]),
                        Tree(Token('RULE', 'and_'), [
                            Tree('event',
                                 [Token('EVENT_NAME', 'CPR')]),
                            Tree('event', [
                                Token('EVENT_NAME', 'MoT')])])]),
                    Tree(Token('RULE', 'bfl_statement'), [
                        Tree('forall', [Tree('equiv', [
                            Tree('event',
                                 [Token('EVENT_NAME', 'CPR')]),
                            Tree('event', [
                                Token('EVENT_NAME',
                                      'CIW')])])])]),
                    Tree(Token('RULE', 'bfl_statement'), [
                        Tree('forall', [Tree('nequiv', [
                            Tree('event',
                                 [Token('EVENT_NAME', 'CPR')]),
                            Tree('event', [
                                Token('EVENT_NAME',
                                      'CIW')])])])]),
                    Tree(Token('RULE', 'bfl_statement'), [
                        Tree('forall', [
                            Tree(Token('RULE', 'implies'), [
                                Tree('neg', [Tree('event', [
                                    Token('EVENT_NAME', 'IS')])]),
                                Tree('neg', [Tree('event', [
                                    Token('EVENT_NAME',
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
