import unittest

from gameoflife.game import game_of_life


class Test_Game(unittest.TestCase):
    def setUp(self):
        cellmap = [[0, 0, 0, 1],
                   [1, 1, 1, 0],
                   [0, 0, 1, 1],
                   [1, 0, 0, 0],
                   [0, 0, 0, 0]]

        cells = [(x, y) for y, row in enumerate(cellmap)
                 for x, cell in enumerate(row) if cell == 1]

        self.nextgen = next(game_of_life(cells))

    def test_under_two_neighbours_dies(self):
        self.assertNotIn((0, 3), self.nextgen)
        self.assertNotIn((0, 1), self.nextgen)

    def test_two_neighbours_lives(self):
        self.assertIn((3, 2), self.nextgen)

    def test_three_neighbours_lives(self):
        self.assertIn((2, 0), self.nextgen)

    def test_over_three_neighbours_dies(self):
        self.assertNotIn((2, 1), self.nextgen)

    def test_blank_under_three_neighbours_blank(self):
        self.assertNotIn((2, 4), self.nextgen)
        self.assertNotIn((0, 4), self.nextgen)

    def test_blank_three_neighbours_born(self):
        self.assertIn((1, 0), self.nextgen)

    def test_blank_over_three_neighbours_blank(self):
        self.assertNotIn((3, 1), self.nextgen)
