import unittest

from life_utils.pop_ups import grid_size_warning


class PopUps(unittest.TestCase):
    def test_grid_size_warning(self):
        self.assertTrue(grid_size_warning(3))
        self.assertTrue(grid_size_warning(4))

        # Turning on test flag because I don't want a window to appear during tests.
        self.assertFalse(grid_size_warning("a", True))
        self.assertFalse(grid_size_warning(2, True))
        self.assertFalse(grid_size_warning(1, True))
        self.assertFalse(grid_size_warning(-1, True))