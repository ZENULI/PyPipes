"""
# This files originate from the "PyPipes" project:
#   https://github.com/ZENULI/PyPipes
# Created by ZENULI at University Paul Sabatier III :
#   https://github.com/BastienKovac
#   https://github.com/Ulynor
#   https://github.com/seb2s
# License:
#   MIT License Copyright (c) 2022 ZENULI
"""

from setuptools import setup, find_packages

with open('README.md') as _f:
    _README_MD = _f.read()

_VERSION = '0.1'

setup(
    name='project', # TODO: rename. 
    version=_VERSION,
    description='An empty project base.',
    long_description=_README_MD,
    classifiers=[
        # TODO: typing.
        "Typing :: Typed"
    ],
    url='https://github.com/..../....',  # TODO.
    download_url='https://github.com/.../.../tarball/{}'.format(_VERSION),  # TODO.
    author='',  # TODO.
    author_email='',  # TODO.
    packages=find_packages(include=['project*']),  # TODO.
    test_suite="testing",
    setup_requires=["pytest-runner"],
    tests_require=["pytest", "pytest-cov"],
    install_requires=[""],
    include_package_data=True,
    license='TODO',  # TODO: set your license string. 
    keywords='empty project TODO keywords'
)

