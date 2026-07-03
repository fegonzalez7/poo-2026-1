import unittest
from unittest.mock import patch

from src.engine.type_relations import TypeRelations
from src.models.move import Move
from src.models.pokemon import Pokemon
from src.models.stats import Stats
from src.models.trainer import Trainer


def make_pokemon(name, types, hp=20, attack=1, defense=0.5, level=1):
    stats = Stats(
        hp=hp,
        attack=attack,
        defense=defense,
        special_attack=1,
        special_defense=1,
        speed=1,
    )
    return Pokemon(name, types, stats, life=hp, attack=attack, defense=defense, level=level)


@patch("src.models.move.time.sleep")
class TestTypeEffectiveness(unittest.TestCase):
    def setUp(self):
        self.relations = TypeRelations()

    def test_fire_super_effective_vs_grass(self, _):
        move = Move("Ember", "Fire", 5, 100, 25)
        attacker = make_pokemon("Charmander", ["Fire"], attack=2)
        defender = make_pokemon("Bulbasaur", ["Grass"])
        life_before = defender.life
        attacker.attack(defender, move, self.relations)
        self.assertLess(defender.life, life_before)

    def test_water_super_effective_vs_fire(self, _):
        move = Move("Water Gun", "Water", 5, 100, 25)
        attacker = make_pokemon("Squirtle", ["Water"], attack=2)
        defender = make_pokemon("Charmander", ["Fire"])
        life_before = defender.life
        attacker.attack(defender, move, self.relations)
        self.assertLess(defender.life, life_before)

    def test_fire_not_effective_vs_water(self, _):
        multiplier = self.relations.get_effectiveness("Fire", ["Water"])
        self.assertEqual(multiplier, 0.5)

    def test_electric_no_effect_vs_ground(self, _):
        move = Move("Thunder", "Electric", 5, 100, 25)
        attacker = make_pokemon("Pikachu", ["Electric"], attack=2)
        defender = make_pokemon("Diglett", ["Ground"])
        life_before = defender.life
        attacker.attack(defender, move, self.relations)
        self.assertEqual(defender.life, life_before)


@patch("src.models.move.time.sleep")
class TestBattleDamage(unittest.TestCase):
    def setUp(self):
        self.relations = TypeRelations()

    def test_life_decreases_after_attack(self, _):
        move = Move("Tackle", "Normal", 5, 100, 25)
        attacker = make_pokemon("A", ["Normal"], attack=2)
        defender = make_pokemon("B", ["Normal"])
        life_before = defender.life
        attacker.attack(defender, move, self.relations)
        self.assertLess(defender.life, life_before)

    def test_life_never_goes_below_zero(self, _):
        move = Move("Overpowered", "Fire", 1000, 100, 25)
        attacker = make_pokemon("A", ["Fire"], attack=100)
        defender = make_pokemon("B", ["Grass"])
        attacker.attack(defender, move, self.relations)
        self.assertGreaterEqual(defender.life, 0)

    def test_defense_reduces_damage(self, _):
        move = Move("Tackle", "Normal", 5, 100, 25)
        attacker = make_pokemon("A", ["Normal"], attack=2)
        low_def = make_pokemon("LowDef", ["Normal"], defense=0.0)
        high_def = make_pokemon("HighDef", ["Normal"], defense=0.9)

        attacker.attack(low_def, move, self.relations)
        attacker.attack(high_def, move, self.relations)

        self.assertLess(low_def.life, high_def.life)

    def test_higher_attack_deals_more_damage(self, _):
        move = Move("Tackle", "Normal", 5, 100, 25)
        weak_attacker = make_pokemon("Weak", ["Normal"], attack=1)
        strong_attacker = make_pokemon("Strong", ["Normal"], attack=5)
        defender1 = make_pokemon("B1", ["Normal"])
        defender2 = make_pokemon("B2", ["Normal"])

        weak_attacker.attack(defender1, move, self.relations)
        strong_attacker.attack(defender2, move, self.relations)

        self.assertLess(defender2.life, defender1.life)


@patch("src.models.move.time.sleep")
class TestTrainerBattle(unittest.TestCase):
    def setUp(self):
        self.charmander = make_pokemon("Charmander", ["Fire"], attack=2)
        self.bulbasaur = make_pokemon("Bulbasaur", ["Grass"])
        self.squirtle = make_pokemon("Squirtle", ["Water"])
        self.trainer1 = Trainer("Ash", "Team1", [self.charmander])
        self.trainer2 = Trainer("Gary", "Team2", [self.bulbasaur, self.squirtle])

    def test_trainer_has_active_pokemon(self, _):
        active = self.trainer1.get_active_pokemon()
        self.assertEqual(active.name, "Charmander")

    def test_trainer_can_switch_pokemon(self, _):
        self.trainer2.switch_pokemon(1)
        active = self.trainer2.get_active_pokemon()
        self.assertEqual(active.name, "Squirtle")

    def test_trainer_max_6_pokemon(self, _):
        trainer = Trainer("Red", "TeamR", [])
        for i in range(7):
            trainer.add_pokemon(make_pokemon(f"Pokemon{i}", ["Normal"]))
        self.assertLessEqual(len(trainer.pokemon), 6)

    def test_trainer_no_duplicate_pokemon(self, _):
        trainer = Trainer("Blue", "TeamB", [])
        p = make_pokemon("Pikachu", ["Electric"])
        trainer.add_pokemon(p)
        trainer.add_pokemon(p)  # duplicado
        self.assertEqual(len(trainer.pokemon), 1)


if __name__ == "__main__":
    unittest.main()
