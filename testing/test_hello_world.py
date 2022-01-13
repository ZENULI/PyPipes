"""
# This files originate from the "" project:
#     https://github.com/
# Created by         at University Paul Sabatier III:
#     https://github.com/
#     https://github.com/
#     https://github.com/
# License:
"""

import pytest

from src.hello_world import hello_world

@pytest.mark.parametrize("argument_values", [True, 1, 1.0])
def test_example(argument_values):
    assert True == argument_values

def test_hello_world(): 
    assert hello_world() == "Hello World!"

