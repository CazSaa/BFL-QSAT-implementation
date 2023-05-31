from os import path

from lark import Lark, Token, Tree

parser = Lark.open(path.join(path.dirname(__file__), "grammar.lark"),
                   start=['start', 'galileo', 'phi', 'psi'])


def parse(text: str) -> Tree[Token]:
    return parser.parse(text, 'start')
