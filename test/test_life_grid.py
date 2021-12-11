import unittest

from PySimpleGUI import Button
import PySimpleGUI

from life_components.life_grid import LifeNode, LifeBoard


class TestLifeNode(unittest.TestCase):
    def setUp(self) -> None:
        self.alive_node = LifeNode([0, 0], alive=True)
        self.dead_node = LifeNode([0, 0], alive=False)

    def test_node_position(self):
        self.assertRaises(TypeError, LifeNode, (0, 0))

    def test_giveth_life(self):
        self.dead_node.giveth_life()
        self.assertTrue(self.dead_node.alive)
        self.assertTrue(self.dead_node.color == "white")

    def test_taketh_life(self):
        self.alive_node.taketh_life()
        self.assertFalse(self.alive_node.alive)
        self.assertTrue(self.alive_node.color == "black")

    def test_life_node_color(self):
        self.assertTrue(self.alive_node.color == "white")
        self.assertTrue(self.dead_node.color == "black")

    def test_life_node_button(self):
        alive_button = self.alive_node.button
        dead_button = self.dead_node.button

        self.assertTrue(alive_button.ButtonColor[1] == "white")
        self.assertTrue(dead_button.ButtonColor[1] == "black")

        # The next tests don't matter whether the node is alive or dead.
        self.assertTrue(type(alive_button) == Button)
        self.assertTrue(alive_button.expand_x)
        self.assertTrue(alive_button.expand_y)
        self.assertTrue(alive_button.Pad[0] == 1)


class TestLifeBoard(unittest.TestCase):
    def setUp(self):
        self.lifeboard = LifeBoard([3, 3])
        grid = self.lifeboard.generate_grid()

        # Abbreviations are cardinal directions.
        # n = North, ne = North-East, etc...
        self.nw_corner_node = LifeNode([0, 0])
        self.ne_corner_node = LifeNode([0, 2])
        self.se_corner_node = LifeNode([2, 2])
        self.sw_corner_node = LifeNode([2, 0])
        self.north_side_node = LifeNode([0, 1])
        self.east_side_node = LifeNode([1, 2])
        self.south_side_node = LifeNode([2, 1])
        self.west_side_node = LifeNode([1, 0])
        self.center_node = LifeNode([1, 1])

    def test_grid_size_type(self):
        self.assertRaises(TypeError, LifeBoard, (1, 1))

    def test_grid_square(self):
        self.assertRaises(ValueError, LifeBoard, [1, 2])

    def test_get_neighbors(self):
        self.assertEqual(
            self.lifeboard.get_neighbors(self.nw_corner_node),
            [None, None, [0, 1], [1, 1], [1, 0], None, None, None])

        self.assertEqual(
            self.lifeboard.get_neighbors(self.ne_corner_node),
            [None, None, None, None, [1, 2], [1, 1], [0, 1], None])

        self.assertEqual(
            self.lifeboard.get_neighbors(self.se_corner_node),
            [[1, 2], None, None, None, None, None, [2, 1], [1, 1]])

        self.assertEqual(
            self.lifeboard.get_neighbors(self.sw_corner_node),
            [[1, 0], [1, 1], [2, 1], None, None, None, None, None])

        self.assertEqual(
            self.lifeboard.get_neighbors(self.north_side_node),
            [None, None, [0, 2], [1, 2], [1, 1], [1, 0], [0, 0], None])

        self.assertEqual(
            self.lifeboard.get_neighbors(self.east_side_node),
            [[0, 2], None, None, None, [2, 2], [2, 1], [1, 1], [0, 1]])

        self.assertEqual(
            self.lifeboard.get_neighbors(self.south_side_node),
            [[1, 1], [1, 2], [2, 2], None, None, None, [2, 0], [1, 0]])

        self.assertEqual(
            self.lifeboard.get_neighbors(self.west_side_node),
            [[0, 0], [0, 1], [1, 1], [2, 1], [2, 0], None, None, None])

        self.assertEqual(
            self.lifeboard.get_neighbors(self.center_node),
            [[0, 1], [0, 2], [1, 2], [2, 2], [2, 1], [2, 0], [1, 0], [0, 0]])

        # TODO:
        # Test that each grid item is a LifeNode..this is hard for some reason.
