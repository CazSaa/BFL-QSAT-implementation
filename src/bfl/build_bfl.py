from functools import lru_cache

from lark import Transformer, Token, Tree
from lark.exceptions import VisitError
from z3 import Bool, And, Or, Implies, Not, ForAll, Exists, Bools, BoolRef, \
    substitute

from bfl.exceptions import BFLError
from galileo.fault_tree import FaultTree
from gates import Gate, VotGate
from utils.get_vars import get_vars
from utils.list_to_tuple import list_to_tuple

CACHE_SIZE = 1000


def build_formula(parse_tree: Tree, fault_tree: FaultTree) -> BoolRef:
    try:
        return BflTransformer(fault_tree).transform(parse_tree)
    except VisitError as e:
        if isinstance(e.orig_exc, BFLError):
            raise e.orig_exc
        raise e


@lru_cache(maxsize=CACHE_SIZE)
def event_to_formula(event: Token | str, fault_tree: FaultTree) -> BoolRef:
    if event not in fault_tree.nodes:
        raise BFLError(f'Unknown event `{event}`')

    # noinspection PyCallingNonCallable
    if fault_tree.in_degree(event) == 0:  # basic event
        return Bool(event)

    if 'gate' not in fault_tree.nodes[event]:
        raise ValueError(f'Event ({event}) does not have gate')

    gate: Gate = fault_tree.nodes[event]['gate']
    return gate.to_z3(*map(lambda e: event_to_formula(e, fault_tree),
                           fault_tree.predecessors(event)))


def replace_with_primes(formula: BoolRef,
                        bes_and_primes: dict[BoolRef, BoolRef]):
    return substitute(formula, *bes_and_primes.items())


def negate_atoms(formula: BoolRef):
    atoms = get_vars(formula)
    return substitute(formula, *zip(atoms, map(Not, atoms)))


# noinspection PyMethodMayBeStatic
class BflTransformer(Transformer):
    def __init__(self, fault_tree: FaultTree):
        super().__init__()
        self.fault_tree = fault_tree
        self.prime_counter = 0

    @list_to_tuple
    @lru_cache(maxsize=CACHE_SIZE)
    def forall(self, args):
        free_vars = get_vars(args[0])
        return ForAll(free_vars, args[0]) if len(free_vars) > 0 else args[0]

    @list_to_tuple
    @lru_cache(maxsize=CACHE_SIZE)
    def exists(self, args):
        free_vars = get_vars(args[0])
        return Exists(free_vars, args[0]) if len(free_vars) > 0 else args[0]

    @list_to_tuple
    @lru_cache(maxsize=CACHE_SIZE)
    def with_evidence(self, args):
        phi, evidence = args
        return ForAll(get_vars(evidence), Implies(evidence, phi))

    @list_to_tuple
    @lru_cache(maxsize=CACHE_SIZE)
    def evidence(self, args):
        return And(*args) if len(args) > 1 else args[0]

    @list_to_tuple
    @lru_cache(maxsize=CACHE_SIZE)
    def mcs(self, args):
        bes_and_primes = self.primes()
        return And(
            args[0],
            Not(Exists(
                list(bes_and_primes.values()),
                And(
                    And(*(Implies(p, b) for b, p in bes_and_primes.items())),
                    Or(*(p != b for b, p in bes_and_primes.items())),
                    replace_with_primes(args[0], bes_and_primes)
                )
            ))
        )

    @list_to_tuple
    @lru_cache(maxsize=CACHE_SIZE)
    def mps(self, args):
        bes_and_primes = self.primes()
        return And(
            negate_atoms(Not(args[0])),
            Not(Exists(
                list(bes_and_primes.values()),
                And(
                    And(*(Implies(p, b) for b, p in bes_and_primes.items())),
                    Or(*(p != b for b, p in bes_and_primes.items())),
                    negate_atoms(
                        replace_with_primes(Not(args[0]), bes_and_primes))
                )
            ))
        )

    @list_to_tuple
    @lru_cache(maxsize=CACHE_SIZE)
    def vot(self, args):
        return VotGate(args[0], int(args[1])).to_z3(*args[2])

    @list_to_tuple
    @lru_cache(maxsize=CACHE_SIZE)
    def basic_events(self, args):
        return tuple((event_to_formula(be, self.fault_tree) for be in args))

    @list_to_tuple
    @lru_cache(maxsize=CACHE_SIZE)
    def mapping(self, args):
        return Bool(args[0].value) if args[1] == '1' \
            else Not(Bool(args[0].value))

    @list_to_tuple
    @lru_cache(maxsize=CACHE_SIZE)
    def and_(self, args):
        return And(*args)

    @list_to_tuple
    @lru_cache(maxsize=CACHE_SIZE)
    def or_(self, args):
        return Or(*args)

    @list_to_tuple
    @lru_cache(maxsize=CACHE_SIZE)
    def implies(self, args):
        return Implies(*args)

    @list_to_tuple
    @lru_cache(maxsize=CACHE_SIZE)
    def equiv(self, args):
        return args[0] == args[1]

    @list_to_tuple
    @lru_cache(maxsize=CACHE_SIZE)
    def nequiv(self, args):
        return args[0] != args[1]

    @list_to_tuple
    @lru_cache(maxsize=CACHE_SIZE)
    def neg(self, args):
        return Not(args[0])

    @list_to_tuple
    @lru_cache(maxsize=CACHE_SIZE)
    def event(self, args):
        return event_to_formula(args[0], self.fault_tree)

    def primes(self) -> dict[BoolRef, BoolRef]:
        self.prime_counter += 1
        bes = self.fault_tree.get_basic_events()
        primes = [be + "'" * self.prime_counter for be in bes]
        as_str = ' '.join(bes + primes)
        bools = Bools(as_str)
        half = len(bools) // 2
        return {bools[i]: bools[i + half] for i in range(half)}
