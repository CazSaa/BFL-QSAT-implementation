from bfl.execute_bfl import execute_bfl
from galileo.build_graph import build_fault_tree
from parser.parser import parse


def main(bfl_text: str):
    return execute_str(bfl_text, True)


def execute_str(bfl_text: str, print_output=False):
    parse_tree = parse(bfl_text)
    fault_tree = build_fault_tree(parse_tree)
    return execute_bfl(parse_tree, fault_tree, print_output)


if __name__ == '__main__':
    main()
