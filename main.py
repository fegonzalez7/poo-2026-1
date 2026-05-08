import time
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


class Move:
    def __init__(self, name: str, type: str, power: float, accuracy: int, pp: int):
        self._name = name
        self._type = type
        self._power = power
        self._accuracy = accuracy
        self._pp = pp

    @property
    def name(self) -> str:
        return self._name

    @property
    def type(self) -> str:
        return self._type

    @property
    def power(self) -> float:
        return self._power

    @property
    def accuracy(self) -> int:
        return self._accuracy

    @property
    def pp(self) -> int:
        return self._pp


class Moveset:
    def __init__(self, moves: List[Move] = None):
        self.moves: List[Move] = []
        if moves:
            for move in moves:
                self.add_move(move)

    def add_move(self, move: Move) -> bool:
        if len(self.moves) < 4:
            self.moves.append(move)
            print(f"¡El Pokémon aprendió {move.name}!")
            time.sleep(0.5)
            return True
        else:
            print(f"El Pokémon intenta aprender {move.name}, pero ya conoce 4 movimientos.")
            time.sleep(0.5)
            return False

    def remove_move(self, index: int) -> bool:
        if 0 <= index < len(self.moves):
            removed_move = self.moves.pop(index)
            print("1, 2 y... ¡Poof!")
            time.sleep(1)
            print(f"El Pokémon olvidó cómo usar {removed_move.name}.")
            time.sleep(0.5)
            return True
        else:
            print("Índice no válido. No se pudo olvidar el movimiento.")
            return False

    def replace_move(self, index: int, new_move: Move) -> bool:
        if 0 <= index < len(self.moves):
            old_move = self.moves[index]
            print("1, 2 y... ¡Poof!")
            time.sleep(1)
            print(f"El Pokémon olvidó cómo usar {old_move.name} y...")
            time.sleep(1)
            self.moves[index] = new_move
            print(f"¡Aprendió {new_move.name}!")
            time.sleep(0.5)
            return True
        else:
            print("Índice no válido. No se pudo reemplazar el movimiento.")
            return False

    def get_moves(self) -> List[Move]:
        return self.moves

    def show_moves(self) -> None:
        if not self.moves:
            print("El Pokémon aún no conoce ningún movimiento.")
            time.sleep(0.5)
        else:
            print("\n" + "="*45)
            print("                 MOVIMIENTOS")
            print("="*45)
            for i, move in enumerate(self.moves):
                print(f"[{i + 1}] {move.name.ljust(12)} | Tipo: {move.type.ljust(8)} | Poder: {str(move.power).ljust(3)} | PP: {move.pp}")
            print("="*45 + "\n")
            time.sleep(0.5)


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
        moveset: Moveset = None,
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

    def attack(
        self, target: "Pokemon", move: Move, relations: TypeRelations
    ) -> None:
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

    # Crear movimientos
    flame_burst = Move(name="Flame Burst", type="Fire", power=5, accuracy=100, pp=25)
    vine_whip = Move(name="Vine Whip", type="Grass", power=5, accuracy=100, pp=25)
    water_gun = Move(name="Water Gun", type="Water", power=5, accuracy=100, pp=25)

    # Crear Pokémon con moveset
    charmander_moveset = Moveset([flame_burst])
    charmander = Pokemon("Charmander", ["Fire"], charmander_stats, life=20, attack=2, moveset=charmander_moveset)

    bulbasaur_moveset = Moveset([vine_whip])
    bulbasaur = Pokemon("Bulbasaur", ["Grass"], bulbasaur_stats, life=20, defense=0.3, moveset=bulbasaur_moveset)

    squirtle_moveset = Moveset([water_gun])
    squirtle = Pokemon("Squirtle", ["Water"], squirtle_stats, life=20, moveset=squirtle_moveset)

    print("\n--- BATTLE 1 ---")
    charmander.attack(bulbasaur, flame_burst, relations)

    print("\n--- BATTLE 2 ---")
    bulbasaur.attack(squirtle, vine_whip, relations)

    print("\n--- BATTLE 3 ---")
    squirtle.attack(charmander, water_gun, relations)


if __name__ == "__main__":
    main()
