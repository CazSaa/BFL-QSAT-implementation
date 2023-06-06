from os import path

from lark import Lark, Token, Tree

with open(path.join(path.dirname(__file__), "grammar.lark")) as g:
    parser = Lark(g,
                  start=['start', 'galileo', 'phi', 'bfl_statement'],
                  maybe_placeholders=False)


def parse(text: str) -> Tree[Token]:
    return parser.parse(text, 'start')
