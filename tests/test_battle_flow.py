from main import Pokemon, Stats, Move, Moveset, Trainer, TypeRelations


def make_strong_pokemon(name="Strong pokemon", speed=10):
    stats = Stats(hp=100, attack=9999, defense=0.1,  # Caso de daño extremo
                  special_attack=1, special_defense=1, speed=speed)
    move = Move(name="Overpowered", type="Fire", power=100,
                accuracy=100, pp=10)
    return Pokemon(name, ["Fire"], stats, life=stats.hp, attack=stats.attack,
                    defense=stats.defense, moveset=Moveset([move]))


def make_weak_pokemon(name="Weak pokemon", speed=1):
    stats = Stats(hp=1, attack=1, defense=0.1,  # Minimo ataque, debe perder claramente contra Strong
                  special_attack=1, special_defense=1, speed=speed)
    move = Move("Tackle", "Grass", 1, 100, 10)
    return Pokemon(name, ["Grass"], stats, life=stats.hp, attack=stats.attack,
                    defense=stats.defense, moveset=Moveset([move]))


# Daño y derrota

def test_attack_reduces_defender_life():
    relations = TypeRelations()
    strong = make_strong_pokemon()
    weak = make_weak_pokemon()

    life_before = weak.life
    strong.attack(weak, strong.moveset.get_moves()[0], relations)

    assert weak.life < life_before


def test_pokemon_faints_after_lethal_attack():
    relations = TypeRelations()
    strong = make_strong_pokemon()
    weak = make_weak_pokemon()

    strong.attack(weak, strong.moveset.get_moves()[0], relations)

    assert weak.life == 0


def test_life_does_not_go_below_zero():
    relations = TypeRelations()
    strong = make_strong_pokemon()
    weak = make_weak_pokemon()

    # Un ataque exageradamente fuerte no debe dejar vida negativa
    strong.attack(weak, strong.moveset.get_moves()[0], relations)
    strong.attack(weak, strong.moveset.get_moves()[0], relations)

    assert weak.life == 0


# Batalla completa simulada turno a turno con los métodos reales de Pokemon

def test_full_battle_declares_a_winner():
    relations = TypeRelations()
    strong = make_strong_pokemon()
    weak = make_weak_pokemon()

    trainer1 = Trainer("Ash", "Team A", [strong])
    trainer2 = Trainer("Misty", "Team B", [weak])

    attacker, defender = trainer1.get_active_pokemon(), trainer2.get_active_pokemon()

    # Se simula la batalla turno a turno usando Pokemon.attack() hasta que
    # uno de los dos se quede sin vida.
    max_turns = 20
    turns = 0
    while attacker.life > 0 and defender.life > 0 and turns < max_turns:
        attacker.attack(defender, attacker.moveset.get_moves()[0], relations)
        attacker, defender = defender, attacker
        turns += 1

    assert strong.life > 0
    assert weak.life == 0


def test_full_battle_with_multiple_rival_pokemon():
    relations = TypeRelations()
    strong = make_strong_pokemon()
    weak1 = make_weak_pokemon("Weak 1")
    weak2 = make_weak_pokemon("Weak 2")

    trainer1 = Trainer("Ash", "Team A", [strong])
    trainer2 = Trainer("Misty", "Team B", [weak1, weak2])

    # Strong derrota al primer Pokémon del equipo rival
    strong.attack(trainer2.get_active_pokemon(), strong.moveset.get_moves()[0], relations)
    assert trainer2.get_active_pokemon().life == 0

    # El rival cambia a su segundo Pokémon y también es derrotado
    trainer2.switch_pokemon(1)
    strong.attack(trainer2.get_active_pokemon(), strong.moveset.get_moves()[0], relations)

    assert weak1.life == 0
    assert weak2.life == 0
    assert strong.life > 0


# Manejo del equipo (Trainer)

def test_switch_changes_active_pokemon():
    p1 = make_strong_pokemon()
    p2 = make_weak_pokemon()

    trainer = Trainer("Ash", "Team A", [p1, p2])
    trainer.switch_pokemon(1)

    assert trainer.get_active_pokemon().name == "Weak pokemon"


def test_add_pokemon_to_team():
    p1 = make_strong_pokemon()
    p2 = make_weak_pokemon("Reserve pokemon")

    trainer = Trainer("Ash", "Team A", [p1])
    trainer.add_pokemon(p2)

    assert p2 in trainer.pokemon
    assert len(trainer.pokemon) == 2


def test_add_pokemon_does_not_duplicate_same_pokemon():
    p1 = make_strong_pokemon()

    trainer = Trainer("Ash", "Team A", [p1])
    trainer.add_pokemon(p1)

    assert trainer.pokemon.count(p1) == 1
