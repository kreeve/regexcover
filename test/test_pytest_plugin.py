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

    
    result.stdout.fnmatch_lines(['Pattern a|b, total 2 covered 1.*'])
    
def test_longer_regex(testdir):
    """Test a longer regex."""
    testdir.makeconftest("""pytest_plugins = ['regexcover']
    """)
    
    testdir.makepyfile("""
    import re
    def test_hello(cover_regex):
      m = re.match('a|b|\d+', 'a')
      cover_regex.assert_called_with('a|b|\d+', 'a')
    """)
    result = testdir.runpytest(re_fail_under=0)
    result.assert_outcomes(passed=1)

    result.stdout.fnmatch_lines(['Pattern a|b|\d+, total 3 covered 1. 33 percent.'])
    

def test_multi_regex(testdir):
    """Multiple regexes, failing with not all covered."""
    testdir.makeconftest("""pytest_plugins = ['regexcover']
    """)
            
    testdir.makepyfile("""
    import re

    def match_regex_thing(text):
      return re.match('hi|hello|\d+', text)

    def test_regex(cover_regex):
      match_regex_thing('hello')
    """)
    result = testdir.runpytest('--re-fail-under=50')
    result.assert_outcomes(passed=1)
    result.stdout.fnmatch_lines(['FAIL: Pattern hi|hello|\d+, total 3 covered 1. 33 percent.'])

def test_multi_regex(testdir):
    """Multiple regexes, failing with not all covered."""
    testdir.makeconftest("""pytest_plugins = ['regexcover']
    """)
            
    testdir.makepyfile("""
    import re

    def match_regex_thing(text):
      return re.match('hi|hello|\d+', text)

    def test_regex(cover_regex):
      match_regex_thing('hello')

    def test_hi(cover_regex):
      match_regex_thing('hi')

    def test_numbers(cover_regex):
      match_regex_thing('125')
    """)
    result = testdir.runpytest('--re-fail-under=100')
    result.assert_outcomes(passed=3)
    result.stdout.fnmatch_lines(['Pattern hi|hello|\d+, total 3 covered 3. 100 percent.'])
