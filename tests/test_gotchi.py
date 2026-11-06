import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from gotchi import (
    PETS,
    ACHIEVEMENTS,
    LEVEL_RANKS,
    draw_bar,
    load_state,
    save_state,
    calculate_xp_and_level,
    STATE_FILE,
)


class TestGotchi(unittest.TestCase):
    def test_pets_structure(self):
        for pet_key in ["cat", "dino", "crab", "dog", "duck", "dragon", "owl"]:
            self.assertIn(pet_key, PETS)
            data = PETS[pet_key]
            self.assertIn("name", data)
            self.assertIn("species", data)
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

    def test_xp_and_level_calculation(self):
        state = {"lifetime_commits": 10, "bonus_commits": 0, "total_pets": 0}
        total_xp, level, rank_title, cur_base, next_goal = calculate_xp_and_level(state, today_commits=5)
        self.assertEqual(total_xp, 15)
        self.assertEqual(level, 1)
        self.assertIn("Intern", rank_title)

        # High XP test
        state_senior = {"lifetime_commits": 200, "bonus_commits": 5, "total_pets": 10}
        total_xp_sr, level_sr, rank_sr, _, _ = calculate_xp_and_level(state_senior, today_commits=20)
        self.assertTrue(total_xp_sr >= 200)
        self.assertTrue(level_sr >= 4)
        self.assertIn("Architect", rank_sr)

    def test_achievements_structure(self):
        self.assertTrue(len(ACHIEVEMENTS) >= 6)
        for ach in ACHIEVEMENTS:
            self.assertIn("id", ach)
            self.assertIn("title", ach)
            self.assertIn("desc", ach)
            self.assertTrue(callable(ach["check"]))


if __name__ == "__main__":
    unittest.main()
