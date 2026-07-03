import unittest
from unittest.mock import patch

from src.models.move import Move, Moveset
from src.models.pokemon import Pokemon
from src.models.stats import Stats


def make_pokemon(name="Charmander", types=None, level=1):
    """Helper para crear Pokémon de prueba rápidamente."""
    if types is None:
        types = ["Fire"]
    stats = Stats(hp=20, attack=2, defense=0.5, special_attack=1, special_defense=1, speed=1)
    return Pokemon(name, types, stats, life=20, level=level)


class TestEvolution(unittest.TestCase):
    """Pruebas del método evolve de Pokemon."""

    def test_evolve_increases_level(self):
        p = make_pokemon(level=1)
        p.evolve(2, "Blaze")
        self.assertEqual(p.level, 2)

    def test_evolve_updates_special_ability(self):
        p = make_pokemon(level=1)
        p.evolve(2, "Blaze")
        self.assertEqual(p.special_ability, "Blaze")

    def test_evolve_to_same_level_fails(self):
        p = make_pokemon(level=5)
        p.evolve(5, "Blaze")
        self.assertEqual(p.level, 5)
        self.assertEqual(p.special_ability, "None")

    def test_evolve_to_lower_level_fails(self):
        p = make_pokemon(level=5)
        p.evolve(3, "Blaze")
        self.assertEqual(p.level, 5)
        self.assertEqual(p.special_ability, "None")

    def test_evolve_multiple_times(self):
        p = make_pokemon(level=1)
        p.evolve(2, "Blaze")
        p.evolve(5, "Inferno")
        p.evolve(10, "Overheat")
        self.assertEqual(p.level, 10)
        self.assertEqual(p.special_ability, "Overheat")

    def test_evolve_does_not_change_name(self):
        p = make_pokemon("Charmander", level=1)
        p.evolve(2, "Blaze")
        self.assertEqual(p.name, "Charmander")

    def test_evolve_does_not_reset_life(self):
        p = make_pokemon(level=1)
        p.life = 10
        p.evolve(2, "Blaze")
        self.assertEqual(p.life, 10)


@patch("src.models.move.time.sleep")
class TestMovesetManagement(unittest.TestCase):
    def test_add_move_up_to_4(self, _):
        moveset = Moveset()
        for i in range(4):
            result = moveset.add_move(Move(f"Move{i}", "Fire", 5, 100, 10))
            self.assertTrue(result)
        self.assertEqual(len(moveset.moves), 4)

    def test_fifth_move_rejected(self, _):
        moveset = Moveset()
        for i in range(4):
            moveset.add_move(Move(f"Move{i}", "Fire", 5, 100, 10))
        result = moveset.add_move(Move("Extra", "Fire", 5, 100, 10))
        self.assertFalse(result)
        self.assertEqual(len(moveset.moves), 4)

    def test_remove_move_valid_index(self, _):
        moveset = Moveset()
        moveset.add_move(Move("Ember", "Fire", 5, 100, 10))
        result = moveset.remove_move(0)
        self.assertTrue(result)
        self.assertEqual(len(moveset.moves), 0)

    def test_remove_move_invalid_index(self, _):
        moveset = Moveset()
        result = moveset.remove_move(5)
        self.assertFalse(result)

    def test_replace_move(self, _):
        moveset = Moveset()
        moveset.add_move(Move("Ember", "Fire", 5, 100, 10))
        new_move = Move("Flamethrower", "Fire", 10, 95, 15)
        result = moveset.replace_move(0, new_move)
        self.assertTrue(result)
        self.assertEqual(moveset.moves[0].name, "Flamethrower")

    def test_replace_move_invalid_index(self, _):
        moveset = Moveset()
        result = moveset.replace_move(3, Move("Flamethrower", "Fire", 10, 95, 15))
        self.assertFalse(result)

if __name__ == "__main__":
    unittest.main()
