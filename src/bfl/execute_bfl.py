from lark import Tree
from lark.reconstruct import Reconstructor
from z3 import Solver, sat, And, Bool, Not, ModelRef, is_true, BoolRef, \
    substitute, BoolVal

from bfl.build_bfl import build_formula, event_to_formula
from galileo.fault_tree import FaultTree
from parser.parser import parser
from utils.all_models import all_models
from utils.get_vars import get_vars


def get_bfl_tree(parse_tree: Tree):
    if parse_tree.data == 'bfl':
        return parse_tree
    if parse_tree.data == 'start':
        assert parse_tree.children[1].data == 'bfl'
        return parse_tree.children[1]
    raise ValueError(f'parse_tree does not contain bfl tree: {parse_tree}')


def reconstruct(parse_tree: Tree):
    terminals = {
        '_EXISTS': lambda _: '\\exists ',
        '_IMPLIES': lambda _: ' => ',
        '_NEG': lambda _: '!',
        '_AND': lambda _: ' && ',
        '_OR': lambda _: ' || ',
        '_EQUIV': lambda _: ' == ',
        '_NEQUIV': lambda _: ' != ',
        '_MODELS': lambda _: ' |= ',
    }
    return Reconstructor(parser, terminals).reconstruct(parse_tree)


def quantified_statement(parse_tree: Tree, fault_tree: FaultTree):
    assert parse_tree.data == 'forall' or parse_tree.data == 'exists'
    s = Solver()
    s.add(build_formula(parse_tree, fault_tree))
    return s.check() == sat


def sup_statement(parse_tree: Tree, fault_tree: FaultTree):
    formula = build_formula(parse_tree.children[0], fault_tree)
    root_formula = event_to_formula(fault_tree.get_root(), fault_tree)
    return are_formulas_independent(formula, root_formula)


def get_dependent_variables(formula: BoolRef) -> set[BoolRef]:
    result = set()

    for var in get_vars(formula):
        s = Solver()
        s.add(substitute(formula, (var, BoolVal(True)))
              != substitute(formula, (var, BoolVal(False))))
        if s.check() == sat:
            result.add(var)

    return result


def idp_statement(parse_tree: Tree, fault_tree: FaultTree):
    assert parse_tree.data == 'idp'
    formula1 = build_formula(parse_tree.children[0], fault_tree)
    formula2 = build_formula(parse_tree.children[1], fault_tree)
    return are_formulas_independent(formula1, formula2)


def are_formulas_independent(formula1, formula2):
    # This could be more efficient because not all variables need to be checked
    # in order to conclude something here. For example, if formula1 only
    # contains one variable, it must only be checked whether this variable is a
    # dependent variable in formula3.
    vars1 = get_dependent_variables(formula1)
    vars2 = get_dependent_variables(formula2)
    return vars1.isdisjoint(vars2)


def get_status_vector(parse_tree: Tree, fault_tree: FaultTree):
    assert parse_tree.data == 'basic_events'
    bes_in_sv = {token.value for token in parse_tree.children}
    all_bes = fault_tree.get_basic_events_set()
    if not bes_in_sv.issubset(all_bes):
        raise ValueError(
            'Status vector can only contain basic events')  # todo test
    bes_not_in_sv = all_bes - bes_in_sv
    return And(*(map(Bool, bes_in_sv)), *(Not(Bool(b)) for b in bes_not_in_sv))


def check_model(parse_tree: Tree, fault_tree: FaultTree):
    assert parse_tree.data == 'check_model'
    status_vector = get_status_vector(parse_tree.children[0], fault_tree)
    formula = build_formula(parse_tree.children[1], fault_tree)
    s = Solver()
    s.add(formula)
    s.add(status_vector)
    return s.check() == sat


def get_true_events(model: ModelRef):
    return frozenset((e for e in model.decls() if is_true(model[e])))


def satisfaction_set(parse_tree: Tree, fault_tree: FaultTree):
    formula = build_formula(parse_tree.children[0], fault_tree)
    s = Solver()
    s.add(formula)
    s.check()
    return set(map(get_true_events,
                   all_models(s, fault_tree.get_basic_events_bools())))


def execute_bfl_statement(parse_tree: Tree, fault_tree: FaultTree):
    match parse_tree.data:
        case 'exists' | 'forall':
            return quantified_statement(parse_tree, fault_tree)
        case 'sup':
            return sup_statement(parse_tree, fault_tree)
        case 'idp':
            return idp_statement(parse_tree, fault_tree)
        case 'check_model':
            return check_model(parse_tree, fault_tree)
        case 'satisfaction_set':
            return satisfaction_set(parse_tree, fault_tree)
        case _:
            raise ValueError('Unknown statement')


def execute_bfl(parse_tree: Tree, fault_tree: FaultTree, print_output=False):
    bfl_tree = get_bfl_tree(parse_tree)
    results = []
    for statement in bfl_tree.children:
        if print_output:
            print(f'Solving {reconstruct(statement)}\n...')

        result = execute_bfl_statement(statement, fault_tree)
        results.append(result)

        if print_output:
            print(result, '\n')

    return results
