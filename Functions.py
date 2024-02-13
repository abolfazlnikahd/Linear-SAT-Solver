from Atom import Atom

from ast import Or
from typing import List, Dict

from And import And
from Not import Not


def parse_horn(formula_str: str):
    tokens = tokenize(formula_str)
    return parse_implies(tokens)


def tokenize(formula_str: str) -> List[str]:
    return formula_str.replace("(", " ( ").replace(")", " ) ").split()


def parse_implies(tokens: List[str]):
    phi = parse_or(tokens)
    if len(tokens) > 0 and tokens[0] == "=>":
        tokens.pop(0)
        psi = parse_implies(tokens)
        phi = And(Not(phi), psi)
    return phi


def parse_or(tokens: List[str]):
    phi = parse_and(tokens)
    while len(tokens) > 0 and tokens[0] == "∨":
        tokens.pop(0)
        psi = parse_and(tokens)
        phi = Or(phi, psi)
    return phi


def parse_and(tokens: List[str]):
    phi = parse_atom(tokens)
    while len(tokens) > 0 and tokens[0] == "∧":
        tokens.pop(0)
        psi = parse_atom(tokens)
        phi = And(phi, psi)
    return phi


def parse_atom(tokens: List[str]):
    token = tokens.pop(0)
    if token == "(":
        phi = parse_implies(tokens)
        tokens.pop(0)  # pop off ")"
        return phi
    elif token.startswith("~"):
        return Not(parse_atom([token[1:]]))
    else:
        return Atom(token)


def is_satisfiable(formula) -> bool:
    atoms = get_atoms(formula)
    for assignment in generate_assignments(atoms):
        if evaluate(formula, assignment):
            return True
    return False


def get_atoms(formula) -> List[str]:
    atoms = set()
    stack = [formula]
    while stack:
        node = stack.pop()
        if isinstance(node, Atom):
            atoms.add(node.name)
        elif isinstance(node, Not):
            stack.append(node.formula)
        elif isinstance(node, And):
            stack.append(node.left)
            stack.append(node.right)
    return list(atoms)


def generate_assignments(atoms: List[str]) -> List[Dict[str, bool]]:
    assignments = []
    for i in range(2 ** len(atoms)):
        assignment = {}
        for j, atom in enumerate(atoms):
            assignment[atom] = bool(i & (1 << j))
        assignments.append(assignment)
    return assignments


def evaluate(formula, assignment: Dict[str, bool]) -> bool:
    if isinstance(formula, Atom):
        return assignment[formula.name]
    elif isinstance(formula, Not):
        return not evaluate(formula.formula, assignment)
    elif isinstance(formula, And):
        return evaluate(formula.left, assignment) and evaluate(formula.right, assignment)
    else:
        raise ValueError("Invalid formula")
