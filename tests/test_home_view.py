import unittest

from ui.components import render_orientation_card, render_page_intro, render_section_intro
from views.home import render_home


class HomeViewSmokeTests(unittest.TestCase):
    def test_home_presentation_components_are_importable(self):
        self.assertTrue(callable(render_home))
        self.assertTrue(callable(render_page_intro))
        self.assertTrue(callable(render_section_intro))
        self.assertTrue(callable(render_orientation_card))


if __name__ == "__main__":
    unittest.main()
