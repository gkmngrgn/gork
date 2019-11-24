import unittest

from gork.palette import get_flat_palette


class GorkTest(unittest.TestCase):
    def test_flat_palette_length(self):
        self.assertEqual(len(get_flat_palette()), 768)
