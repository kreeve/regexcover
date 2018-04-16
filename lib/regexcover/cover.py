import re
import sre_compile
import sre_constants
import sre_parse

def split_toplevel(parsed):
    """Split a parsed regex by OR blocks."""
    if parsed[0][0] == sre_constants.IN:
        return [[p] for p in parsed[0][1]]
    if parsed[0][0] == sre_constants.BRANCH:
        return parsed[0][1][1]
    return parsed

def record_matches(split, text):
    """Record which clauses match."""
    matches = frozenset()
    for clause in split:
        p = sre_parse.Pattern()
        scanner = sre_compile.compile(sre_parse.SubPattern(p, clause))\
                             .scanner(text)
        if scanner.match():
            matches |= {tuple(clause)}

    return matches

def num_matches(split, text):
    return len(record_matches(split, text))
