from regexcover import plugin

def test_simple_regex(testdir):
    """Make sure the plugin works."""
    testdir.makeconftest("""pytest_plugins = ['regexcover']
    """)
    
    testdir.makepyfile("""
    import re
    def test_hello(cover_regex):
      m = re.match('a|b', 'a')
      cover_regex.assert_called_with('a|b', 'a')
    """)
    result = testdir.runpytest()
    result.assert_outcomes(passed=1)

    
    result.stdout.fnmatch_lines(['Pattern a|b, total 2 covered 1.'])
    
def test_longer_regex(testdir):
    """Make sure the plugin works."""
    testdir.makeconftest("""pytest_plugins = ['regexcover']
    """)
    
    testdir.makepyfile("""
    import re
    def test_hello(cover_regex):
      m = re.match('a|b|\d+', 'a')
      cover_regex.assert_called_with('a|b|\d+', 'a')
    """)
    result = testdir.runpytest()
    result.assert_outcomes(passed=1)

    result.stdout.fnmatch_lines(['Pattern a|b|\d+, total 3 covered 1.'])
    
