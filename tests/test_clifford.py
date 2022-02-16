import pytest
from qps.clifford import Tableau


def test_hh():
    tab = Tableau(1)
    tab.hadamard(0)
    tab.hadamard(0)
    assert tab.measure(0) == 0

def test_x():
    tab = Tableau(1)
    tab.hadamard(0)
    tab.phase(0)
    tab.phase(0)
    tab.hadamard(0)
    assert tab.measure(0) == 1

def test_measure():
    for _ in range(100):
        tab = Tableau(1)
        tab.hadamard(0)
        assert tab.measure(0) == tab.measure(0)

@pytest.mark.parametrize('nbits', [*range(10, 101, 10)])
def test_ghz(nbits):
    tab = Tableau(nbits)
    tab.hadamard(0)
    for i in range(nbits - 1):
        tab.cnot(i, i+1)
    res = [tab.measure(i) for i in range(nbits)]
    assert all(res) or not any(res)
