import sre_parse

import regexcover

def test_basic_regex():
    parsed = sre_parse.parse('a|b|\d+')
    split = regexcover.split_toplevel(parsed)
    matches = regexcover.record_matches(split, '1234')
    assert len(matches) == 1

