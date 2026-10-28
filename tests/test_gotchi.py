import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from gotchi import (
    PETS,
    draw_bar,
    load_state,
    save_state,
    STATE_FILE,
)


class TestGotchi(unittest.TestCase):
    def test_pets_structure(self):
        for pet_key in ["cat", "dino", "crab"]:
            self.assertIn(pet_key, PETS)
            data = PETS[pet_key]
            self.assertIn("name", data)
            self.assertIn("godmode", data)
            self.assertIn("super_happy", data)
            self.assertIn("happy", data)
            self.assertIn("hungry", data)
            self.assertIn("dead", data)

    def test_draw_bar(self):
        bar_full = draw_bar(100, 100, width=10)
        self.assertEqual(bar_full, "█" * 10)

        bar_empty = draw_bar(0, 100, width=10)
        self.assertEqual(bar_empty, "░" * 10)

        bar_half = draw_bar(50, 100, width=10)
        self.assertEqual(bar_half, "█" * 5 + "░" * 5)

    def test_state_load(self):
        state = load_state()
        self.assertIsInstance(state, dict)
        self.assertIn("happiness", state)


if __name__ == "__main__":
    unittest.main()
