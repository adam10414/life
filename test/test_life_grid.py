import unittest

from PySimpleGUI import Button

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

    def test_taketh_life(self):
        self.alive_node.taketh_life()
        self.assertFalse(self.alive_node.alive)

    def test_life_node_color(self):
        self.assertTrue(self.alive_node.color == "white")
        self.assertTrue(self.dead_node.color == "black")

    def test_life_node_button(self):
        alive_button = self.alive_node.button()
        dead_button = self.dead_node.button()

        self.assertTrue(alive_button.ButtonColor[1] == "white")
        self.assertTrue(dead_button.ButtonColor[1] == "black")

        # The next tests don't matter whether the node is alive or dead.
        self.assertTrue(type(alive_button) == Button)
        self.assertTrue(alive_button.expand_x)
        self.assertTrue(alive_button.expand_y)
        self.assertTrue(alive_button.Pad[0] == 1)


class TestLifeBoard(unittest.TestCase):
    def test_grid_size_type(self):
        self.assertRaises(TypeError, LifeBoard, (1, 1))

    def test_grid_square(self):
        self.assertRaises(ValueError, LifeBoard, [1, 2])
