This extends `pytest` to count the percentage of a regex exercised by `re.match` in Python programs. A regular expression match of the form `re.match('a|b', 'a')` should report 50% coverage, but existing coverage tools would report it as 100% coverage.

# Motivation

I've had to debug some regex-heavy code recently, and I noticed it was all reporting 100% coverage on statements like `re.match('a|b', 'a')`. Despite there being no actual branching in the code, the regular expression itself essentially "branches" to either match `a` or `b`. This package aims to capture that notion.

# Example

You can install with

```
pip install git+git://github.com/kreeve/regexcover.git
```

1. Create a simple program.


```
pytest_plugins = ['regexcover']
def match_regex_thing(text):
    return re.match('hi|hello|\d+', text)

def test_regex():
    match_regex_thing('hello')


```

Run it with `pytest`:

```
pytest test.py --re-fail-under=100
```

and observe the test suite fails due to lack of coverage! Add another test case:



```
pytest_plugins = ['regexcover']
def match_regex_thing(text):
    return re.match('hi|hello|\d+', text)

def test_regex():
    match_regex_thing('hello')

def test_hi():
    match_regex_thing('hi')

def test_numbers():
    match_regex_thing('125')
```

Running the same command will now give you a pass!

# Cautionary Note
I found myself dealing with a regex-heavy project and had to do what I could with it. I would recommend not using regex as heavily over trying to use this project!

# Future Work
This is currently a toy project, but I plan to develop it further if/when I get time.

- Support further nested regexes. Right now `'a|(b|c)|d` will show 30% coverage for the string `'b'`, but it really should break the second clause into `b` and `c`.
- Maybe some HTML reporting!
