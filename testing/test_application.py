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