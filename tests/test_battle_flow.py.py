import pytest
from .main import Pokemon, Stats, Move, Moveset, Trainer, Field


def make_strong_pokemon(name="Strong pokemon", speed=10):
    stats = Stats(hp=100, attack=9999, defense=0.1, #Caso de daño extremo
                  special_attack=1, special_defense=1, speed=speed)
    move = Move(name = "Overpowered", type = "Fire", power = 100, 
                  accuracy = 100, pp = 10)
    return Pokemon(name, ["Fire"], stats, moveset=Moveset([move]))


def make_weak_pokemon(name="Weak pokemon", speed=1):
    stats = Stats(hp=1, attack=1, defense=0.1,  #Minimo ataque, debe ganar claramente Strong
                  special_attack=1, special_defense=1, speed=speed)
    move = Move("Tackle", "Grass", 1, 100, 10)
    return Pokemon(name, ["Grass"], stats, moveset=Moveset([move]))


#Para los turnos

def test_faster_pokemon_goes_first(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "1") #Se usa monkeypatch para evitar el input

    fast = make_strong_pokemon()
    slow = make_weak_pokemon()

    trainer1 = Trainer("Ash", "Team A", [fast])
    trainer2 = Trainer("Misty", "Team B", [slow])

    field = Field(trainer1, trainer2)
    order = field.determine_turn_order()

    assert order[0].name == "Strong pokemon"
    assert order[1].name == "Weak pokemon"


def test_equal_speed_order_is_one_of_two_valid(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "1")

    p1 = make_strong_pokemon(speed=5)
    p2 = make_weak_pokemon(speed=5)

    trainer1 = Trainer("Ash", "Team A", [p1])
    trainer2 = Trainer("Misty", "Team B", [p2])

    field = Field(trainer1, trainer2)
    order = field.determine_turn_order()

    assert set(p.name for p in order) == {"Strong pokemon", "Weak pokemon"}


#Condición de fin de batalla


def test_battle_finished_when_one_fainted(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "1")

    alive = make_strong_pokemon()
    fainted = make_weak_pokemon()
    fainted.stats.hp = 0

    trainer1 = Trainer("Ash", "Team A", [alive])
    trainer2 = Trainer("Misty", "Team B", [fainted])
    field = Field(trainer1, trainer2)

    assert field.battle_finished([alive, fainted]) is True


def test_battle_not_finished_when_all_alive(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "1")

    p1 = make_strong_pokemon(name="P1")
    p2 = make_weak_pokemon(name="P2")

    trainer1 = Trainer("Ash", "Team A", [p1])
    trainer2 = Trainer("Misty", "Team B", [p2])
    field = Field(trainer1, trainer2)

    assert field.battle_finished([p1, p2]) is False

#Ataque y derrota

def test_pokemon_faints_after_lethal_attack(monkeypatch):
    inputs = iter(["1", "1"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs, "1"))

    strong = make_strong_pokemon()
    weak = make_weak_pokemon()

    trainer1 = Trainer("Ash", "Team A", [strong])
    trainer2 = Trainer("Misty", "Team B", [weak])

    Field(trainer1, trainer2).battlefield()

    assert weak.is_fainted()
    assert weak.stats.hp == 0


def test_winner_has_at_least_one_pokemon_alive(monkeypatch):
    inputs = iter(["1", "1"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs, "1"))

    strong = make_strong_pokemon()
    weak = make_weak_pokemon()

    trainer1 = Trainer("Ash", "Team A", [strong])
    trainer2 = Trainer("Misty", "Team B", [weak])

    Field(trainer1, trainer2).battlefield()

    assert not strong.is_fainted()


def test_loser_has_no_pokemon_alive(monkeypatch):
    inputs = iter(["1", "1"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs, "1"))

    strong = make_strong_pokemon()
    weak = make_weak_pokemon()

    trainer1 = Trainer("Ash", "Team A", [strong])
    trainer2 = Trainer("Misty", "Team B", [weak])

    Field(trainer1, trainer2).battlefield()

    assert weak.is_fainted()


#Relevo de Pokémon


def test_next_pokemon_available_when_active_faints():
    fainted = make_weak_pokemon()
    fainted.stats.hp = 0
    reserve = make_weak_pokemon()

    trainer = Trainer("Ash", "Team A", [fainted, reserve])

    assert trainer.get_next_available_pokemon_index() == 1


def test_no_next_pokemon_when_all_fainted():
    p1 = make_weak_pokemon()
    p2 = make_weak_pokemon()
    p1.stats.hp = 0
    p2.stats.hp = 0

    trainer = Trainer("Ash", "Team A", [p1, p2])

    assert trainer.get_next_available_pokemon_index() is None


def test_switch_changes_active_pokemon():
    p1 = make_strong_pokemon()
    p2 = make_weak_pokemon()

    trainer = Trainer("Ash", "Team A", [p1, p2])
    trainer.switch_pokemon(1)

    assert trainer.get_active_pokemon().name == "Weak pokemon"

#Batalla

@pytest.mark.parametrize("inputs, weak_fainted, strong_fainted, description", [
    (
        ["1", "1"],
        True, False,
        "Ataca y continúa: débil cae de un golpe, fuerte sobrevive"
    ),
    (
        ["1", "3"],
        True, False,
        "Ataca y se rinde: débil ya cayó antes de que se procese la rendición"
    ),
    (
        ["1", "2", "1", "1"],
        True, False,
        "Ataca, intenta cambiar Pokémon (índice 1), continúa: débil igual cae"
    ),
    (
        ["1", "1", "1", "1"],
        True, False,
        "Ataca dos turnos seguidos: débil cae en el primero, segundo turno no llega"
    ),
    (
        ["1", "1"],
        True, False,
        "Equipo rival con dos débiles: el fuerte derrota al primero y gana"
    ),
])
def test_battlefield_parametrize(monkeypatch, inputs, weak_fainted, strong_fainted, description):
    respuestas = iter(inputs)
    monkeypatch.setattr("builtins.input", lambda _: next(respuestas, "1"))

    strong = make_strong_pokemon()
    weak   = make_weak_pokemon()

    trainer1 = Trainer("Ash",   "Team A", [strong])
    trainer2 = Trainer("Misty", "Team B", [weak])

    Field(trainer1, trainer2).battlefield()

    assert weak.is_fainted()   == weak_fainted,   f"FALLÓ [{description}]"
    assert strong.is_fainted() == strong_fainted, f"FALLÓ [{description}]"


# Batalla con varios pokemon

def test_full_battle_team_exhausted(monkeypatch):
    # inputs: por cada Pokémon rival se da movimiento 1, luego continuar
    #El fuerte derrota al equipo rival uno por uno
    inputs = iter(["1", "1", "1", "1"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs, "1"))

    strong = make_strong_pokemon()
    weak1  = make_weak_pokemon()
    weak2  = make_weak_pokemon()

    trainer1 = Trainer("Ash",   "Team A", [strong])
    trainer2 = Trainer("Misty", "Team B", [weak1, weak2])

    Field(trainer1, trainer2).battlefield()

    assert all(p.is_fainted() for p in trainer2.pokemon)
    assert not strong.is_fainted()
    