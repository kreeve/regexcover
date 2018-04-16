from __future__ import absolute_import

from .cover import split_toplevel, num_matches
from collections import defaultdict
from unittest import mock

import sre_parse
import re
import pytest


def pytest_configure(config):
    config.pluginmanager.register(RegexCoverage(config), 'RegexCoverage')

def pytest_addoption(parser):
    """Add command-line options for this plugin."""
    group = parser.getgroup('recov', 'Regular expression coverage.')
    group.addoption('--re-fail-under', action='store',
                    metavar='MIN', type=int,
                    default=50,
                    help='Fail if any regular expression\'s coverage is less than MIN.')
    
class RegexCoverage(object):
    def __init__(self, options):
        self.covered_clauses = defaultdict(lambda: 0)
        self.total_clauses = {}
        self.original_parse = re.match
        self.config = options
        
    def match(self, pattern, text):
        parsed = sre_parse.parse(pattern)
        split = split_toplevel(parsed)
        if isinstance(split, list):
            self.total_clauses[pattern] = len(split)
            self.covered_clauses[pattern] += num_matches(split, text)
            return mock.Mock()
        return self.original_parse(pattern, text)
    
    @pytest.fixture(scope='session')
    def cover_regex(self):
        """Add coverage to all regex."""
        with mock.patch('re.match', side_effect=self.match) as re_mock:
            yield re_mock

    def pytest_terminal_summary(self, terminalreporter):
        """Write results to console."""
        for pattern, num in self.total_clauses.items():
            num_covered = self.covered_clauses[pattern]
            kwargs = dict(red=True, green=False)
            if float(num_covered)/float(num) < self.config.getoption('--re-fail-under'):
                kwargs = dict(red=False, green=True)
            terminalreporter.write('\n\nPattern {}, total {} covered {}.\n'\
                                   .format(pattern, num, num_covered), **kwargs)
            
    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtestloop(self, session):
        yield

        for pattern, num in self.total_clauses.items():
            num_covered = self.covered_clauses[pattern]
            if float(num_covered)/float(num) < self.config.getoption('--re-fail-under'):
                session.testsfailed += 1
