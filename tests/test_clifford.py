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
