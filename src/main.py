import argparse
import sys

from lark import UnexpectedInput

from bfl.execute_bfl import execute_bfl
from galileo.build_graph import build_fault_tree
from parser.parser import parse


def main(bfl_text: str):
    try:
        return execute_str(bfl_text, True)
    except UnexpectedInput as e:
        print(f'Parse error:\n{e}', file=sys.stderr)


def execute_str(bfl_text: str, print_output=False):
    parse_tree = parse(bfl_text)
    fault_tree = build_fault_tree(parse_tree)
    return execute_bfl(parse_tree, fault_tree, print_output)


if __name__ == '__main__':
    argparser = argparse.ArgumentParser(
        description='Executes a BFL file and prints the results.')
    argparser.add_argument('file',
                           help='path to the BFL file you want to execute',
                           type=argparse.FileType('r'))
    args = argparser.parse_args()
    try:
        file_text = args.file.read()
    finally:
        args.file.close()
    main(file_text)
