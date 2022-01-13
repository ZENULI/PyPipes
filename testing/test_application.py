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

from testing.tests.installation_test import installation_test01
from testing.tests.nn_test import nn_test01
from testing.tests.reconstruct_test import reconstruct_test01

@pytest.mark.parametrize("argument_values", [True, 1, 1.0])
def test_installation(argument_values):
    assert installation_test01() == argument_values

def test_neuralnetwork():
    assert nn_test01() == "NeuralNet"

def test_reconstruct():
    assert reconstruct_test01() == 0