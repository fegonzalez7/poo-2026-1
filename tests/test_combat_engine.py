import unittest
from unittest.mock import patch

from src.engine.combat_engine import CombatEngine
from src.models.move import Move
from src.models.pokemon import Pokemon
from src.models.stats import Stats


def make_pokemon(name, types, hp=20, attack=2, defense=0.5, level=1):
    stats = Stats(
        hp=hp,
        attack=attack,
        defense=defense,
        special_attack=1,
        special_defense=1,
        speed=1,
    )
    return Pokemon(name, types, stats, life=hp, attack=attack, defense=defense, level=level)


class TestHitAccuracy(unittest.TestCase):
    def test_returns_tuple_of_bool_and_float(self):
        move = Move("Ember", "Fire", 5, 100, 25)
        result = CombatEngine.hit_accuracy(move, ["Grass"])
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], bool)
        self.assertIsInstance(result[1], float)

    def test_effectiveness_super_effective(self):
        move = Move("Ember", "Fire", 5, 100, 25)
        _, effect = CombatEngine.hit_accuracy(move, ["Grass"])
        self.assertEqual(effect, 2.0)

    def test_effectiveness_not_very_effective(self):
        move = Move("Ember", "Fire", 5, 100, 25)
        _, effect = CombatEngine.hit_accuracy(move, ["Water"])
        self.assertEqual(effect, 0.5)

    def test_effectiveness_immune(self):
        move = Move("Thunder", "Electric", 5, 100, 25)
        _, effect = CombatEngine.hit_accuracy(move, ["Ground"])
        self.assertEqual(effect, 0.0)

    def test_high_accuracy_hits_most_of_the_time(self):
        move = Move("Ember", "Fire", 5, 100, 25)
        hits = sum(1 for _ in range(100) if CombatEngine.hit_accuracy(move, ["Normal"])[0])
        self.assertGreater(hits, 90)

    def test_zero_accuracy_never_hits(self):
        move = Move("Miss", "Fire", 5, 0, 25)
        hits = sum(1 for _ in range(50) if CombatEngine.hit_accuracy(move, ["Normal"])[0])
        self.assertEqual(hits, 0)


class TestCalculateDamage(unittest.TestCase):
    @patch("src.models.move.time.sleep")
    def setUp(self, mock_sleep):
        self.move = Move("Ember", "Fire", 5, 100, 25)
        self.attacker = make_pokemon("Charmander", ["Fire"], attack=2, level=5)
        self.defender = make_pokemon("Bulbasaur", ["Grass"], defense=0.5, level=5)

    def test_damage_is_non_negative(self):
        damage = CombatEngine.calculate_damage(self.attacker, self.defender, self.move)
        self.assertGreaterEqual(damage, 0)

    def test_damage_zero_on_miss(self):
        weak_move = Move("Miss", "Fire", 5, 0, 25)
        damages = [
            CombatEngine.calculate_damage(self.attacker, self.defender, weak_move)
            for _ in range(20)
        ]
        self.assertTrue(all(d == 0 for d in damages))

    def test_higher_level_attacker_deals_more_damage(self):
        low_level = make_pokemon("Low", ["Fire"], attack=2, level=1)
        high_level = make_pokemon("High", ["Fire"], attack=2, level=10)

        with patch("src.engine.combat_engine.random.random", return_value=0.01):
            damage_low = CombatEngine.calculate_damage(low_level, self.defender, self.move)
            damage_high = CombatEngine.calculate_damage(high_level, self.defender, self.move)

        self.assertGreater(damage_high, damage_low)

    def test_super_effective_deals_more_than_neutral(self):
        fire_move = Move("Ember", "Fire", 5, 100, 25)
        normal_move = Move("Tackle", "Normal", 5, 100, 25)

        with patch("src.engine.combat_engine.random.random", return_value=0.01):
            damage_super = CombatEngine.calculate_damage(self.attacker, self.defender, fire_move)
            damage_neutral = CombatEngine.calculate_damage(
                self.attacker, self.defender, normal_move
            )

        self.assertGreater(damage_super, damage_neutral)


if __name__ == "__main__":
    unittest.main()
