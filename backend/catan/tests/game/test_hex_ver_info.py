import pytest
from catan.cargaJson import HexagonInfo


class TestInfo:
    def test_hexaInfo(self):
        neighbors = HexagonInfo(0, 0)
        assert neighbors == [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5]]
