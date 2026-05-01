from typing import List


class TypeRelations:
    def __init__(self) -> None:
        self.type_chart: dict[str, dict[str, float]] = {
            "Fire": {
                "Fire": 0.5,
                "Water": 0.5,
                "Grass": 2.0,
                "Electric": 1.0,
                "Ground": 1.0,
            },
            "Water": {
                "Fire": 2.0,
                "Water": 0.5,
                "Grass": 0.5,
                "Electric": 1.0,
                "Ground": 2.0,
            },
            "Grass": {
                "Fire": 0.5,
                "Water": 2.0,
                "Grass": 0.5,
                "Electric": 1.0,
                "Ground": 2.0,
            },
            "Electric": {
                "Fire": 1.0,
                "Water": 2.0,
                "Grass": 0.5,
                "Electric": 0.5,
                "Ground": 0.0,
            },
            "Ground": {
                "Fire": 2.0,
                "Water": 1.0,
                "Grass": 0.5,
                "Electric": 2.0,
                "Ground": 1.0,
            },
        }

    def get_effectiveness(self, attack_type: str, defender_types: List[str]) -> float:
        multiplier: float = 1.0

        for defender in defender_types:
            if attack_type in self.type_chart:
                if defender in self.type_chart[attack_type]:
                    multiplier = multiplier * self.type_chart[attack_type][defender]
                else:
                    multiplier = multiplier * 1.0
            else:
                multiplier = multiplier * 1.0

        return multiplier


class Stats:
    def __init__(
        self,
        hp: float,
        attack: float,
        defense: float,
        special_attack: float,
        special_defense: float,
        speed: float,
    ):
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.special_attack = special_attack
        self.special_defense = special_defense
        self.speed = speed

    def __str__(self):
        return (
            f"HP: {self.hp}, ",
            f"Attack: {self.attack}, Defense: {self.defense}, "
            f"Sp. Attack: {self.special_attack}, Sp. Defense: {self.special_defense}, ",
            f"Speed: {self.speed}",
        )


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
    ) -> None:
        self.name = name
        self.types = types
        self.life = life
        self.attack_power = attack
        self.stats = stats
        self.defense = defense
        self.level = level
        self.special_ability = special_ability

    def get_stats(self) -> str:
        return f"{self.name} Stats: {self.stats}"

    def attack(
        self, target: "Pokemon", base_power: float, relations: TypeRelations
    ) -> None:
        attack_type = self.types[0]

        multiplier = relations.get_effectiveness(attack_type, target.types)

        damage = base_power * self.attack_power * multiplier

        print(f"{self.name} attacks {target.name}")
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

"""
%TAREA%
Implementar la clase CombatEngine con un método calculate_damage(): Esta función recibirá al attacker (Pokémon), al defender (Pokémon) y al move (Movimiento).
Integrar Dependencias (Composición): Dentro de calculate_damage, debe usar (llamar a) los objetos y sus métodos:

    El nivel y ataque del attacker (de pokemon.level y pokemon.stats).
    La defensa del defender (de pokemon.stats).
    El poder del movimiento (de move.power).
    La efectividad del tipo (llamando al get_effectiveness de la instancia de TypeRelations).

Implementar hit_accuracy(): Añadir lógica para determinar si un movimiento acierta o falla.
"""

"""Asumiendo que existe class Move con las siguientes caracteristicas:
Move: Debe contener los atributos de un ataque: name, type (string), power, accuracy, y pp.
"""
class CombatEngine:
    @staticmethod
    def hit_accuracy(attack: Move, defender_types: List[str]):
        import random 
        tp = TypeRelations()
        effect = tp.get_effectiveness(attack.type, defender_types)
        factor = random.random()
        
        return  attack.accuracy > (factor*effect)/(factor+1), effect # si es mayor entonces el ataque acierta

    @staticmethod
    def calculate_damage(attacker: Pokemon, defender: Pokemon, move: Move):
        att_stats = attacker.stats
        def_stats = defender.stats
        is_able_to_attack, multiplier = CombatEngine.hit_accuracy(move, defender.types)
        # tener en cuenta quien tiene mas nivel
        rlevel = (attacker.level/defender.level) 
        # tener en cuenta si atacante tiene mas ataque que la defensa del defensa
        rdef = (att_stats.attack/def_stats.defense)
        # ataque -> si is_able_to_attack = 0 entonces ataque fallido, sino, calcular ataque
        damage = int(is_able_to_attack)*(rlevel*rdef*multiplier*move.power)
        print(f"Damage: {damage}")
        return damage




class Trainer:
    def __init__(self, nombre: str, team: str, pokemon: List[Pokemon]):
        self.nombre = nombre
        self.team = team
        self.pokemon = pokemon if pokemon is not None else []

    def add_pokemon(self, pokemon: Pokemon):
        if len(self.pokemon) < 6 and pokemon not in self.pokemon:
            self.pokemon.append(pokemon)
        else:
            print("No se puede agregar más Pokémon o el Pokémon ya está en el equipo.")

    def get_active_pokemon(self):
        if self.pokemon:
            return self.pokemon[0]
        else:
            print("No tienes Pokémon en tu equipo.")
            return None

    def switch_pokemon(self, pokemon_index):
        if 0 <= pokemon_index < len(self.pokemon):
            self.pokemon[0], self.pokemon[pokemon_index] = (
                self.pokemon[pokemon_index],
                self.pokemon[0],
            )
        else:
            print("Indice de Pokémon no valido.")


def main() -> None:
    relations = TypeRelations()

    charmander_stats = Stats(
        hp=20, attack=2, defense=0.5, special_attack=1, special_defense=1, speed=1
    )
    bulbasaur_stats = Stats(
        hp=20, attack=1, defense=0.3, special_attack=1, special_defense=1, speed=1
    )
    squirtle_stats = Stats(
        hp=20, attack=1, defense=0.5, special_attack=1, special_defense=1, speed=1
    )

    charmander = Pokemon("Charmander", ["Fire"], charmander_stats, life=20, attack=2)
    bulbasaur = Pokemon("Bulbasaur", ["Grass"], bulbasaur_stats, life=20, defense=0.3)
    squirtle = Pokemon("Squirtle", ["Water"], squirtle_stats, life=20)

    print("\n--- BATTLE 1 ---")
    charmander.attack(bulbasaur, base_power=5, relations=relations)

    print("\n--- BATTLE 2 ---")
    bulbasaur.attack(squirtle, base_power=5, relations=relations)

    print("\n--- BATTLE 3 ---")
    squirtle.attack(charmander, base_power=5, relations=relations)


if __name__ == "__main__":
    main()
