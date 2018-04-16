from setuptools import setup, find_packages
import sys

if sys.version_info < (3, 4):
    sys.exit('Sorry, Python < 3.4 is not supported')

setup(
    author="Kyle Reeve",
    author_email='krzw92@gmail.com',
    description="Regex match shouldn't show 100% coverage.",
    entry_points={
        'pytest11': [
            'regexcover = regexcover.plugin'
        ]
    },
    classifiers=[
        "Framework :: Pytest",
        'Programming Language :: Python :: 3.6',
        'Development Status :: 2 - Pre-Alpha'
    ],
    install_requires=[],
    include_package_data=True,
    keywords='regexcover',
    name='regexcover',
    package_dir={'': 'lib'},
    packages=find_packages('lib'),
    version='0.1.0',
)
