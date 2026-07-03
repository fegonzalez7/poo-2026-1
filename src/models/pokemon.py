from typing import List

from src.engine.type_relations import TypeRelations
from src.models.move import Move, Moveset
from src.models.stats import Stats


class Pokemon:
    def __init__(
        self,
        name: str,
        types: List[str],
        stats: Stats,
        life: float = 10,
        attack: float = 1,
        defense: float = 0.5,
        level: int = 1,
        special_ability: str = "None",
        moveset: Moveset | None = None,
    ) -> None:
        self.name = name
        self.types = types
        self.life = life
        self.attack_power = attack
        self.stats = stats
        self.defense = defense
        self.level = level
        self.special_ability = special_ability
        self.moveset = moveset if moveset else Moveset()

    def get_stats(self) -> str:
        return f"{self.name} Stats: {self.stats}"

    def attack(self, target: "Pokemon", move: Move, relations: TypeRelations) -> None:
        attack_type = move.type

        multiplier = relations.get_effectiveness(attack_type, target.types)

        damage = move.power * self.attack_power * multiplier

        print(f"{self.name} attacks {target.name} with {move.name}")
        print(f"Effectiveness: x{multiplier}")

        target.defender(damage)

    def defender(self, damage: float) -> None:
        damage_received = damage * (1 - self.defense)

        self.life = self.life - damage_received

        if self.life < 0:
            self.life = 0

        print(f"{self.name} received {damage_received:.2f} damage")
        print(f"Remaining life: {self.life:.2f}")

    def evolve(self, new_level: int, new_ability: str) -> None:
        if new_level > self.level:
            self.level = new_level
            self.special_ability = new_ability
            print(f"{self.name} evolved to level {self.level}")
        else:
            print("Cannot evolve to same or lower level")
