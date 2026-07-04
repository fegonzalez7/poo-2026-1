from src.engine.type_relations import TypeRelations
from src.models.move import Move, Moveset
from src.models.pokemon import Pokemon
from src.models.stats import Stats


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
    charmander = Pokemon(
        "Charmander",
        ["Fire"],
        charmander_stats,
        life=20,
        attack=2,
        moveset=charmander_moveset,
    )

    bulbasaur_moveset = Moveset([vine_whip])
    bulbasaur = Pokemon(
        "Bulbasaur",
        ["Grass"],
        bulbasaur_stats,
        life=20,
        defense=0.3,
        moveset=bulbasaur_moveset,
    )

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
